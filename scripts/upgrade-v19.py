#!/usr/bin/env python3
"""Bring the v1.8 packaged project to the Android 7–17 v1.9 release target."""
from pathlib import Path
from textwrap import dedent
p=Path(".")
java=p/"app/src/main/java/com/pomodoro/focus"
(p/"build.gradle").write_text("plugins {\n    id 'com.android.application' version '9.4.0' apply false\n}\n")
(p/"app/build.gradle").write_text(dedent("""\
    plugins { id 'com.android.application' }
    android {
        namespace 'com.pomodoro.focus'
        compileSdk 37
        defaultConfig {
            applicationId 'com.pomodoro.focus'
            minSdk 24
            targetSdk 37
            versionCode 11
            versionName '1.9'
        }
    }
"""))
f=java/"FocusTileService.java"
s=f.read_text()
s=s.replace("import android.os.Handler;", "import android.os.Build;\nimport android.os.Handler;")
s=s.replace("        tile.setSubtitle(subtitle);", "        if (Build.VERSION.SDK_INT >= 29) tile.setSubtitle(subtitle);")
f.write_text(s)
f=java/"TimerNotifications.java"
s=f.read_text()
s=s.replace("        Notification notification = new Notification.Builder(context, CHANNEL)\n",
"""        Notification.Builder completeBuilder = Build.VERSION.SDK_INT >= 26
                ? new Notification.Builder(context, CHANNEL)
                : new Notification.Builder(context);
        Notification notification = completeBuilder
""")
f.write_text(s)
f=java/"MainActivity.java"
s=f.read_text()
s=s.replace("import android.app.Activity;", "import android.Manifest;\nimport android.app.Activity;\nimport android.content.pm.PackageManager;\nimport android.os.Build;")
s=s.replace(
"""        getWindow().getDecorView().setSystemUiVisibility(android.view.View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
                | android.view.View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);""",
"""        int uiFlags = android.view.View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR;
        if (Build.VERSION.SDK_INT >= 26) uiFlags |= android.view.View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
        getWindow().getDecorView().setSystemUiVisibility(uiFlags);""")
s=s.replace('        view.loadUrl("file:///android_asset/index.html");',
"""        view.loadUrl("file:///android_asset/index.html");
        if (Build.VERSION.SDK_INT >= 33 &&
                checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, 20);
        }""")
f.write_text(s)
manifest=p/"app/src/main/AndroidManifest.xml"
s=manifest.read_text().replace('@drawable/ic_launcher','@mipmap/ic_launcher')
manifest.write_text(s)
# Adaptive icon: no double rounded-square / white backing on Android 8+
res=p/"app/src/main/res"
(res/"mipmap-anydpi-v26").mkdir(exist_ok=True,parents=True)
(res/"mipmap-xxxhdpi").mkdir(exist_ok=True,parents=True)
(res/"drawable-nodpi").mkdir(exist_ok=True,parents=True)
(res/"values").mkdir(exist_ok=True,parents=True)
(res/"mipmap-anydpi-v26/ic_launcher.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
  <background android:drawable="@color/icon_background"/>
  <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
""")
(res/"values/colors.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<resources><color name="icon_background">#FA6858</color></resources>
""")
# Both legacy and adaptive icons are generated at build time from the same layers.
from PIL import Image, ImageDraw
size=768
fg=Image.new('RGBA',(size,size),(0,0,0,0))
d=ImageDraw.Draw(fg)
d.ellipse((145,190,630,666), fill='#EE4939')
d.ellipse((177,212,594,609), fill='#FA5948')
d.ellipse((224,226,345,267), fill=(255,205,194,155))
d.polygon([(384,191),(336,157),(292,178),(349,215),(271,232),(302,264),
(382,229),(448,264),(479,226),(418,215),(469,177),(426,161)], fill='#36B46B')
d.ellipse((366,158,409,201), fill='#20975A')
d.arc((242,293,527,578),36,336,fill=(255,255,255,240),width=25)
d.ellipse((366,425,402,460), fill='white')
d.line((384,442,384,341),fill='white',width=26)
d.line((384,442,456,484),fill='white',width=24)
fg.save(res/"drawable-nodpi/ic_launcher_foreground.png",optimize=True)
bg=Image.new("RGBA",(size,size),"#FA6858")
bg.alpha_composite(fg)
bg.resize((384,384),Image.Resampling.LANCZOS).convert('RGB').save(res/"mipmap-xxxhdpi/ic_launcher.png",optimize=True)
bg.resize((256,256),Image.Resampling.LANCZOS).convert('RGB').save(p/"app/src/main/assets/logo.png",optimize=True)
(res/"drawable-nodpi/ic_launcher.png").unlink(missing_ok=True)
print("v1.9 target API 37, min API 24, backward compatibility and icon applied")
