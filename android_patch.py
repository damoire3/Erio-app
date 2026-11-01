import os
M = 'android/app/src/main/AndroidManifest.xml'
s = open(M, encoding='utf-8').read()
for p in ['android.permission.POST_NOTIFICATIONS', 'android.permission.SCHEDULE_EXACT_ALARM', 'android.permission.VIBRATE', 'android.permission.USE_FULL_SCREEN_INTENT']:
    if p not in s:
        s = s.replace('<application', '<uses-permission android:name="%s"/>\n    <application' % p, 1)
if os.environ.get('WIDGET') == 'true':
    pkg = 'com.eriomad.app300'
    base = 'android/app/src/main'
    os.makedirs(base + '/java/' + pkg.replace('.', '/'), exist_ok=True)
    for d in ['layout', 'xml', 'drawable']:
        os.makedirs(base + '/res/' + d, exist_ok=True)
    open(base + '/java/' + pkg.replace('.', '/') + '/QuoteWidget.java', 'w', encoding='utf-8').write('''package com.eriomad.app300;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.widget.RemoteViews;
import org.json.JSONArray;

public class QuoteWidget extends AppWidgetProvider {
  static String pick(Context c, boolean advance) {
    try {
      SharedPreferences sp = c.getSharedPreferences("CapacitorStorage", Context.MODE_PRIVATE);
      JSONArray a = new JSONArray(sp.getString("erio_quotes", "[]"));
      if (a.length() == 0) return "Ouvre Erio et ajoute une citation.";
      SharedPreferences st = c.getSharedPreferences("erio_widget", Context.MODE_PRIVATE);
      int i = st.getInt("i", 0);
      if (advance) { i = (i + 1) % a.length(); st.edit().putInt("i", i).apply(); }
      return a.getString(i % a.length());
    } catch (Exception e) { return "Erio"; }
  }
  static void draw(Context c, AppWidgetManager m, int id, boolean adv) {
    RemoteViews v = new RemoteViews(c.getPackageName(), R.layout.widget_quote);
    v.setTextViewText(R.id.quote, "\\u00AB " + pick(c, adv) + " \\u00BB");
    Intent i = new Intent(c, QuoteWidget.class);
    i.setAction("ERIO_NEXT");
    v.setOnClickPendingIntent(R.id.root, PendingIntent.getBroadcast(c, 0, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE));
    m.updateAppWidget(id, v);
  }
  @Override public void onUpdate(Context c, AppWidgetManager m, int[] ids) { for (int id : ids) draw(c, m, id, true); }
  @Override public void onReceive(Context c, Intent in) {
    super.onReceive(c, in);
    if ("ERIO_NEXT".equals(in.getAction())) {
      AppWidgetManager m = AppWidgetManager.getInstance(c);
      for (int id : m.getAppWidgetIds(new ComponentName(c, QuoteWidget.class))) draw(c, m, id, true);
    }
  }
}
''')
    open(base + '/res/drawable/widget_bg.xml', 'w').write('<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle"><solid android:color="#E6161126"/><corners android:radius="22dp"/></shape>')
    open(base + '/res/layout/widget_quote.xml', 'w').write('''<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" android:id="@+id/root" android:layout_width="match_parent" android:layout_height="match_parent" android:orientation="vertical" android:padding="16dp" android:gravity="center" android:background="@drawable/widget_bg">
  <TextView android:id="@+id/quote" android:layout_width="match_parent" android:layout_height="wrap_content" android:gravity="center" android:textColor="#ECE8F8" android:textSize="15sp" android:fontFamily="serif" android:maxLines="6"/>
  <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="ERIO" android:textColor="#B9A2FF" android:textSize="10sp" android:layout_marginTop="8dp"/>
</LinearLayout>''')
    open(base + '/res/xml/quote_widget_info.xml', 'w').write('<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android" android:minWidth="250dp" android:minHeight="110dp" android:updatePeriodMillis="1800000" android:initialLayout="@layout/widget_quote" android:resizeMode="horizontal|vertical" android:widgetCategory="home_screen"/>')
    rcv = '<receiver android:name=".QuoteWidget" android:exported="true"><intent-filter><action android:name="android.appwidget.action.APPWIDGET_UPDATE"/></intent-filter><meta-data android:name="android.appwidget.provider" android:resource="@xml/quote_widget_info"/></receiver>'
    if 'QuoteWidget' not in s:
        s = s.replace('</application>', rcv + '</application>', 1)
open(M, 'w', encoding='utf-8').write(s)
print('patch ok', os.environ.get('WIDGET'))
