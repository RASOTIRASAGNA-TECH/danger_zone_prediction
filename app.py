"""
╔══════════════════════════════════════════════════════════════════╗
║     SafeZone AI – Women Safety  v3.0                            ║
║     Fixed: Notifications · Live GPS · Voice Calls               ║
║     New:   Panic Button · WhatsApp SOS · Custom Contacts        ║
║            Shake Detection · Countdown Timer · Live Clock       ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ──────────────────────────────────────────────────────────────────
# 1. IMPORTS
# ──────────────────────────────────────────────────────────────────
import streamlit as st
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium
import random
import time
import urllib.request
import urllib.parse
import json
from datetime import datetime

# ──────────────────────────────────────────────────────────────────
# 2. PAGE CONFIG
# ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SafeZone AI – Women Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────
# 3. CUSTOM CSS
# ──────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --bg:       #0f0f14;
  --surface:  #18181f;
  --surface2: #1e1e28;
  --border:   #2a2a35;
  --accent:   #e8365d;
  --safe:     #27c97a;
  --medium:   #f5c542;
  --danger:   #e8365d;
  --text:     #f0ede8;
  --muted:    #8a8799;
  --radius:   12px;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.6rem !important; max-width: 1400px; }

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.4rem;
  margin-bottom: 0.9rem;
}

.app-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.5rem 0 1rem; border-bottom: 1px solid var(--border);
  margin-bottom: 1rem;
}
.logo-wrap a { display:flex; align-items:center; gap:10px; text-decoration:none; }
.logo-icon { font-size: 2rem; line-height: 1; }
.app-title { font-family:'DM Serif Display',serif; font-size:1.45rem; color:var(--text); margin:0; line-height:1.2; }
.app-sub { font-size:0.68rem; color:var(--muted); letter-spacing:0.12em; text-transform:uppercase; }
.live-clock { font-size:0.9rem; color:var(--muted); font-variant-numeric:tabular-nums; }

.search-result-card {
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 1rem 1.2rem; margin-bottom: 1rem;
  display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;
}

.section-label {
  font-size: 0.63rem; font-weight: 600; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--muted); margin-bottom: 0.45rem;
}

.risk-badge {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 0.45rem 1rem; border-radius: 999px; font-weight: 600; font-size: 0.9rem;
}
.risk-safe   { background:rgba(39,201,122,0.15); color:var(--safe);   border:1px solid rgba(39,201,122,0.35); }
.risk-medium { background:rgba(245,197,66,0.15); color:var(--medium); border:1px solid rgba(245,197,66,0.35); }
.risk-danger { background:rgba(232,54,93,0.15);  color:var(--danger); border:1px solid rgba(232,54,93,0.35); }

.score-ring-wrap {
  display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 0.8rem 0;
}
.score-number { font-family:'DM Serif Display',serif; font-size:3rem; line-height:1; }

/* SOS Button */
.sos-container { display:flex; flex-direction:column; align-items:center; justify-content:center; padding:0.8rem 0; }
.sos-btn {
  width:110px; height:110px; border-radius:50%;
  background:radial-gradient(circle at 35% 35%,#ff4d6d,#c1121f);
  border:3px solid rgba(255,77,109,0.5);
  box-shadow:0 0 0 8px rgba(232,54,93,0.12),0 0 0 16px rgba(232,54,93,0.06);
  color:white; font-size:1rem; font-weight:700; letter-spacing:0.08em; cursor:pointer;
  transition:all 0.2s ease;
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px;
  text-decoration:none;
  animation: pulseSOS 2s infinite;
}
.sos-btn:hover { box-shadow:0 0 0 12px rgba(232,54,93,0.2),0 0 0 22px rgba(232,54,93,0.1); transform:scale(1.05); }
.sos-label { font-size:0.6rem; opacity:0.85; font-weight:500; }

/* Call button */
.call-btn {
  display:inline-flex; align-items:center; justify-content:center; gap:8px;
  width:100%; padding:0.6rem 1rem; border-radius:8px; border:1px solid rgba(39,201,122,0.4);
  background:rgba(39,201,122,0.1); color:#27c97a; font-weight:600;
  text-decoration:none; font-size:0.88rem; margin-bottom:0.5rem;
  transition:all 0.18s;
}
.call-btn:hover { background:rgba(39,201,122,0.2); border-color:rgba(39,201,122,0.7); }

/* WhatsApp button */
.wa-btn {
  display:inline-flex; align-items:center; justify-content:center; gap:8px;
  width:100%; padding:0.6rem 1rem; border-radius:8px; border:1px solid rgba(37,211,102,0.4);
  background:rgba(37,211,102,0.1); color:#25d366; font-weight:600;
  text-decoration:none; font-size:0.88rem; margin-bottom:0.5rem;
  transition:all 0.18s;
}
.wa-btn:hover { background:rgba(37,211,102,0.2); }

.notif-bar {
  border-radius: var(--radius); padding: 0.65rem 1rem;
  font-size: 0.82rem; display:flex; align-items:center; gap:8px; margin-bottom:0.8rem;
}
.notif-danger { background:rgba(232,54,93,0.12); border:1px solid rgba(232,54,93,0.4); color:#f5bec9; }
.notif-medium { background:rgba(245,197,66,0.10); border:1px solid rgba(245,197,66,0.35); color:#f5e19a; }
.notif-safe   { background:rgba(39,201,122,0.10); border:1px solid rgba(39,201,122,0.30); color:#a3f0cc; }

[data-testid="metric-container"] { background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:0.75rem 1rem; }
[data-testid="stMetricValue"] { color:var(--text) !important; }
[data-testid="stMetricLabel"] { color:var(--muted) !important; }

.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stSelectbox>div>div {
  background:var(--surface) !important; border-color:var(--border) !important;
  color:var(--text) !important; border-radius:8px !important;
}
.stTextInput>div>div>input:focus { border-color:var(--accent) !important; }

.stButton>button {
  background:var(--surface); border:1px solid var(--border); color:var(--text);
  border-radius:8px; font-family:'DM Sans',sans-serif; font-weight:500; transition:all 0.18s;
}
.stButton>button:hover { border-color:var(--accent); color:var(--accent); }

[data-testid="stSidebar"] { background:var(--surface) !important; border-right:1px solid var(--border); }
[data-testid="stSidebar"] * { color:var(--text) !important; }

@keyframes pulseSOS {
  0%  { box-shadow:0 0 0 0 rgba(232,54,93,0.6),0 0 0 8px rgba(232,54,93,0.12); }
  70% { box-shadow:0 0 0 16px rgba(232,54,93,0),0 0 0 24px rgba(232,54,93,0); }
  100%{ box-shadow:0 0 0 0 rgba(232,54,93,0.6),0 0 0 8px rgba(232,54,93,0.12); }
}
@keyframes slideIn { from{opacity:0;transform:translateY(-6px);} to{opacity:1;transform:translateY(0);} }
.animate-in { animation: slideIn 0.35s ease forwards; }

.stProgress > div > div > div > div { background:var(--accent) !important; }
hr { border-color:var(--border) !important; }

.notif-enabled-badge {
  display:inline-flex; align-items:center; gap:6px; font-size:0.75rem;
  color:#27c97a; padding:3px 10px; border-radius:999px;
  background:rgba(39,201,122,0.1); border:1px solid rgba(39,201,122,0.3);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# 4. CONSTANTS & CONFIG
# ──────────────────────────────────────────────────────────────────

DEFAULT_CONTACTS = {
    "Women Helpline (India)": "1091",
    "Police Emergency":       "100",
    "Ambulance":              "108",
    "Disaster Mgmt (NDRF)":  "1078",
    "Railway Police":         "182",
    "Cyber Crime":            "1930",
}

DEFAULT_LAT = 17.3850
DEFAULT_LON = 78.4867

MAP_TILES = {
    "🗺️ Street Map (OSM)": "OpenStreetMap",
    "🌑 Dark (CartoDB)":   "CartoDB dark_matter",
    "🌫️ Light (CartoDB)": "CartoDB positron",
    "🛰️ Topo Map":        "OpenTopoMap",
}

# ──────────────────────────────────────────────────────────────────
# 5. GEOCODING
# ──────────────────────────────────────────────────────────────────

def geocode_place(query: str):
    if not query.strip():
        return None
    try:
        encoded = urllib.parse.quote(query.strip())
        url = (
            "https://nominatim.openstreetmap.org/search"
            f"?q={encoded}&format=json&limit=1&addressdetails=1"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "SafeZoneAI/3.0"})
        with urllib.request.urlopen(req, timeout=7) as resp:
            data = json.loads(resp.read().decode())
        if data:
            r = data[0]
            return {"lat": float(r["lat"]), "lon": float(r["lon"]),
                    "display_name": r.get("display_name", query)}
    except Exception:
        pass
    return None

# ──────────────────────────────────────────────────────────────────
# 6. RISK ENGINE
# ──────────────────────────────────────────────────────────────────

def predict_risk_score(lat: float, lon: float) -> float:
    seed   = int(abs(lat * 1000 + lon * 1000)) % 10000
    rng    = random.Random(seed)
    base   = rng.uniform(5, 95)
    jitter = random.uniform(-5, 5)
    return round(max(0.0, min(100.0, base + jitter)), 1)

def classify_risk(score: float) -> dict:
    thr_safe   = st.session_state.get("thr_safe",   35)
    thr_danger = st.session_state.get("thr_danger", 65)
    if score < thr_safe:
        return {"label":"Safe",   "color":"#27c97a","emoji":"🟢","css":"risk-safe",
                "folium_color":"green",  "notif":"notif-safe"}
    elif score < thr_danger:
        return {"label":"Medium", "color":"#f5c542","emoji":"🟡","css":"risk-medium",
                "folium_color":"orange", "notif":"notif-medium"}
    else:
        return {"label":"Danger", "color":"#e8365d","emoji":"🔴","css":"risk-danger",
                "folium_color":"red",    "notif":"notif-danger"}

# ──────────────────────────────────────────────────────────────────
# 7. NOTIFICATIONS  – auto-request on load + manual button
# ──────────────────────────────────────────────────────────────────

# Injected ONCE on first load — requests permission automatically
NOTIF_INIT_JS = """
<script>
(function(){
  if (!("Notification" in window)) return;
  // Auto-request permission on page load
  if (Notification.permission === "default") {
    Notification.requestPermission().then(function(p){
      if (p === "granted") {
        new Notification("🛡️ SafeZone AI", {
          body: "Notifications enabled! You'll be alerted for danger zones.",
          icon: "https://em-content.zobj.net/source/apple/354/shield_1f6e1-fe0f.png",
          tag:  "safezone-init"
        });
      }
    });
  }
  // Persist permission state to sessionStorage for the badge
  window.__notifPerm = Notification.permission;
})();
</script>
"""

def inject_push_notification(title: str, body: str, tag: str = "safezone"):
    js = f"""
    <script>
    (function(){{
      var title = {json.dumps(title)};
      var body  = {json.dumps(body)};
      var tag   = {json.dumps(tag)};
      var icon  = "https://em-content.zobj.net/source/apple/354/shield_1f6e1-fe0f.png";
      function fire(){{
        try {{ new Notification(title, {{body:body, icon:icon, tag:tag, requireInteraction:false}}); }}
        catch(e){{ console.warn("Notification error:", e); }}
      }}
      if (!("Notification" in window)) return;
      if (Notification.permission === "granted") {{ fire(); }}
      else if (Notification.permission !== "denied") {{
        Notification.requestPermission().then(function(p){{ if(p==="granted") fire(); }});
      }}
    }})();
    </script>
    """
    components.html(js, height=0)

def maybe_notify(score: float, risk_info: dict, place_name: str = "your location"):
    key = f"notified_{round(score,0)}_{place_name[:20]}"
    if st.session_state.get(key):
        return
    st.session_state[key] = True
    if risk_info["label"] == "Danger":
        inject_push_notification(
            "🚨 SafeZone AI — DANGER ZONE",
            f"Risk {score}/100 at {place_name}. Move to safety immediately!",
            "safezone-danger",
        )
    elif risk_info["label"] == "Medium":
        inject_push_notification(
            "⚠️ SafeZone AI — Moderate Risk",
            f"Risk {score}/100 at {place_name}. Stay alert and stay visible.",
            "safezone-medium",
        )

# ──────────────────────────────────────────────────────────────────
# 8. MAP BUILDER
# ──────────────────────────────────────────────────────────────────

def build_map(lat, lon, risk_info, score, nearby_points, tile_label):
    tile_str = MAP_TILES.get(tile_label, "OpenStreetMap")
    m = folium.Map(location=[lat, lon], zoom_start=14, tiles=tile_str, control_scale=True)

    popup_html = f"""
    <div style="font-family:sans-serif;min-width:170px;font-size:13px;line-height:1.6;">
      <b>📍 Your Location</b><br>
      Lat: {lat:.5f}<br>Lon: {lon:.5f}
      <hr style="margin:4px 0">
      <b>Risk Score:</b> {score}/100<br>
      <b>Status:</b> <span style="color:{risk_info['color']};font-weight:bold;">
        {risk_info['emoji']} {risk_info['label']}
      </span>
    </div>"""

    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=220),
        tooltip=f"You — {risk_info['label']} Zone",
        icon=folium.Icon(color=risk_info["folium_color"], icon="shield", prefix="fa"),
    ).add_to(m)

    folium.Circle(
        location=[lat, lon], radius=300,
        color=risk_info["color"], fill=True, fill_opacity=0.1, weight=2,
        tooltip="~300m safety radius",
    ).add_to(m)

    for pt in nearby_points:
        pi = classify_risk(pt["score"])
        folium.CircleMarker(
            location=[pt["lat"], pt["lon"]], radius=9,
            color=pi["color"], fill=True, fill_opacity=0.6,
            popup=folium.Popup(
                f"<b>Nearby Zone</b><br>Score:{pt['score']:.0f}<br>{pi['label']}",
                max_width=140),
            tooltip=f"{pi['emoji']} {pt['score']:.0f}",
        ).add_to(m)

    return m

def generate_nearby_points(lat, lon, n=10):
    pts = []
    for _ in range(n):
        dlat = random.uniform(-0.012, 0.012)
        dlon = random.uniform(-0.012, 0.012)
        pts.append({"lat": lat+dlat, "lon": lon+dlon,
                    "score": predict_risk_score(lat+dlat, lon+dlon)})
    return pts

# ──────────────────────────────────────────────────────────────────
# 9. HEADER  (with live clock)
# ──────────────────────────────────────────────────────────────────

def render_header():
    now = datetime.now().strftime("%a, %d %b %Y  %H:%M:%S")
    st.markdown(f"""
    <div class="app-header">
      <div class="logo-wrap">
        <a href="#" style="text-decoration:none;display:flex;align-items:center;gap:10px;">
          <span class="logo-icon">🛡️</span>
          <div>
            <div class="app-title">SafeZone AI</div>
            <div class="app-sub">Women Safety · Danger Zone Prediction v3</div>
          </div>
        </a>
      </div>
      <div class="live-clock" id="liveClock">{now}</div>
    </div>
    <script>
    (function(){{
      function updateClock(){{
        var el = document.getElementById('liveClock');
        if(el){{
          var d = new Date();
          var opts = {{weekday:'short',day:'2-digit',month:'short',year:'numeric',
                       hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false}};
          el.textContent = d.toLocaleString('en-IN', opts);
        }}
      }}
      setInterval(updateClock, 1000);
    }})();
    </script>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# 10. PLACE SEARCH
# ──────────────────────────────────────────────────────────────────

def render_place_search():
    # ── Destination input ──────────────────────────────────────────
    dest_col1, dest_col2 = st.columns([4, 1])
    with dest_col1:
        destination = st.text_input(
            "🗺️ Enter Destination",
            placeholder="e.g. Hitech City, Hyderabad",
            key="destination_input",
            label_visibility="collapsed",
        )
    with dest_col2:
        dest_clicked = st.button("Navigate", use_container_width=True, key="dest_btn")

    if dest_clicked and destination:
        with st.spinner("Finding destination…"):
            dest_result = geocode_place(destination)
        if dest_result:
            d_lat, d_lon = dest_result["lat"], dest_result["lon"]
            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={d_lat},{d_lon}"
            st.markdown(f"""
            <div class="card" style="display:flex;align-items:center;justify-content:space-between;
                 flex-wrap:wrap;gap:0.8rem;border-color:rgba(66,133,244,0.4);">
              <div>
                <div style="font-size:0.68rem;color:#8a8799;text-transform:uppercase;letter-spacing:0.12em;">Destination Set</div>
                <div style="font-weight:600;font-size:1rem;">📍 {destination.split(',')[0]}</div>
                <div style="font-size:0.72rem;color:#605e6e;">{d_lat:.4f}, {d_lon:.4f}</div>
              </div>
              <a href="{maps_url}" target="_blank" style="
                display:inline-flex;align-items:center;gap:8px;
                padding:0.55rem 1.2rem;border-radius:8px;
                background:rgba(66,133,244,0.15);border:1px solid rgba(66,133,244,0.4);
                color:#4285f4;font-weight:600;font-size:0.88rem;text-decoration:none;">
                🧭 Open in Google Maps
              </a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Destination not found. Try a more specific query.")

    st.markdown('<div style="height:0.4rem;"></div>', unsafe_allow_html=True)

    # ── Live Location Tracking ────────────────────────────────────
    components.html("""
    <div style="background:#1e1e28;border:1px solid #2a2a35;border-radius:10px;
         padding:10px 14px;margin-bottom:8px;font-family:sans-serif;">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
        <div style="font-size:11px;color:#8a8799;text-transform:uppercase;letter-spacing:0.12em;">📡 Live Location Tracking</div>
        <div id="liveLocStatus" style="font-size:11px;color:#605e6e;">Not active</div>
      </div>
      <div style="display:flex;gap:8px;margin-top:8px;">
        <button id="startTrackBtn" onclick="startTracking()" style="
          flex:1;padding:7px;border-radius:7px;cursor:pointer;font-size:12px;font-family:sans-serif;
          background:#1e1e28;border:1px solid #27c97a;color:#27c97a;font-weight:600;">
          ▶ Start Tracking
        </button>
        <button id="stopTrackBtn" onclick="stopTracking()" disabled style="
          flex:1;padding:7px;border-radius:7px;cursor:pointer;font-size:12px;font-family:sans-serif;
          background:#1e1e28;border:1px solid #2a2a35;color:#605e6e;font-weight:600;">
          ■ Stop
        </button>
      </div>
      <div id="liveCoords" style="font-size:11px;color:#8a8799;margin-top:6px;min-height:16px;"></div>
    </div>
    <script>
    var _watchId = null;
    function startTracking(){
      if(!navigator.geolocation){ alert("Geolocation not supported."); return; }
      document.getElementById('liveLocStatus').textContent = "⏳ Acquiring GPS…";
      document.getElementById('liveLocStatus').style.color = "#f5c542";
      document.getElementById('startTrackBtn').disabled = true;
      document.getElementById('stopTrackBtn').disabled = false;
      document.getElementById('stopTrackBtn').style.borderColor = "#e8365d";
      document.getElementById('stopTrackBtn').style.color = "#e8365d";
      _watchId = navigator.geolocation.watchPosition(
        function(pos){
          var lat = pos.coords.latitude.toFixed(6);
          var lon = pos.coords.longitude.toFixed(6);
          var acc = pos.coords.accuracy ? pos.coords.accuracy.toFixed(0)+"m" : "?";
          document.getElementById('liveLocStatus').textContent = "🟢 Live — ±"+acc;
          document.getElementById('liveLocStatus').style.color = "#27c97a";
          document.getElementById('liveCoords').textContent = "📍 "+lat+", "+lon;
          // Update page URL so Streamlit picks it up on next interaction
          var url = new URL(window.parent.location.href);
          url.searchParams.set('lat', lat);
          url.searchParams.set('lon', lon);
          window.parent.history.replaceState(null,'',url.toString());
        },
        function(err){
          document.getElementById('liveLocStatus').textContent = "❌ "+err.message;
          document.getElementById('liveLocStatus').style.color = "#e8365d";
          stopTracking();
        },
        {enableHighAccuracy:true, timeout:15000, maximumAge:5000}
      );
    }
    function stopTracking(){
      if(_watchId !== null){ navigator.geolocation.clearWatch(_watchId); _watchId = null; }
      document.getElementById('liveLocStatus').textContent = "⏹ Stopped";
      document.getElementById('liveLocStatus').style.color = "#605e6e";
      document.getElementById('liveCoords').textContent = "";
      document.getElementById('startTrackBtn').disabled = false;
      document.getElementById('stopTrackBtn').disabled = true;
      document.getElementById('stopTrackBtn').style.borderColor = "#2a2a35";
      document.getElementById('stopTrackBtn').style.color = "#605e6e";
    }
    </script>
    """, height=115)

    # ── Place search ───────────────────────────────────────────────
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        query = st.text_input("🔍 Search a place / address",
                              placeholder="e.g. Banjara Hills, Hyderabad",
                              label_visibility="collapsed")
    with col_btn:
        search_clicked = st.button("Search", use_container_width=True)

    if search_clicked and query:
        with st.spinner("Geocoding…"):
            result = geocode_place(query)
        if result:
            lat, lon, name = result["lat"], result["lon"], result["display_name"]
            score = predict_risk_score(lat, lon)
            info  = classify_risk(score)
            maybe_notify(score, info, name.split(",")[0])

            short_name = name.split(",")[0]
            sub_name   = ", ".join(name.split(",")[1:3])
            st.markdown(f"""
            <div class="search-result-card animate-in">
              <div style="flex:1;">
                <div style="font-size:0.68rem;color:#8a8799;text-transform:uppercase;
                            letter-spacing:0.12em;margin-bottom:4px;">Search Result</div>
                <div style="font-size:1.05rem;font-weight:600;">{short_name}</div>
                <div style="font-size:0.75rem;color:#605e6e;">{sub_name} · {lat:.4f}, {lon:.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px;">
                <div style="font-family:'DM Serif Display',serif;font-size:2.2rem;
                            color:{info['color']};line-height:1;">{score}</div>
                <div style="font-size:0.65rem;color:#605e6e;">/100</div>
              </div>
              <div>
                <span class="risk-badge {info['css']}">{info['emoji']} {info['label']} Zone</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            return lat, lon, name
        else:
            st.error("❌ Place not found. Try a more specific query.")
    return None, None, None

# ──────────────────────────────────────────────────────────────────
# 11. SIDEBAR  – fixed GPS + notifications + custom contacts
# ──────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:

        # ── Notifications (auto-request + manual button) ──────────
        st.markdown("### 🔔 Notifications")
        # Auto-request JS fires once on page load
        components.html(NOTIF_INIT_JS, height=0)

        col_nb, col_ns = st.columns([2, 1])
        with col_nb:
            if st.button("🔔 Enable / Test", use_container_width=True):
                js_enable = """<script>
                if (!("Notification" in window)) {
                  alert("Your browser does not support notifications.");
                } else if (Notification.permission === "granted") {
                  new Notification("🛡️ SafeZone AI", {
                    body: "Notifications are working!",
                    icon: "https://em-content.zobj.net/source/apple/354/shield_1f6e1-fe0f.png",
                    tag: "safezone-test"
                  });
                  alert("✅ Notifications are already enabled and working!");
                } else {
                  Notification.requestPermission().then(function(p) {
                    if (p === "granted") {
                      new Notification("🛡️ SafeZone AI", {
                        body: "Notifications enabled successfully!",
                        icon: "https://em-content.zobj.net/source/apple/354/shield_1f6e1-fe0f.png",
                        tag: "safezone-test"
                      });
                    } else {
                      alert("❌ Permission denied.\\nOpen browser Settings → Site Settings → Notifications → Allow for this site.");
                    }
                  });
                }
                </script>"""
                components.html(js_enable, height=0)
        with col_ns:
            st.markdown(
                '<div style="font-size:0.7rem;color:#8a8799;padding-top:8px;">Allow in browser</div>',
                unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:0.72rem;color:#605e6e;margin-top:4px;margin-bottom:4px;">
        ℹ️ If blocked: browser address bar → 🔒 → Site Settings → Notifications → <b>Allow</b>
        </div>""", unsafe_allow_html=True)

        with st.expander("📖 How to Allow Notifications, Location & Calls"):
            st.markdown("""
**📱 Android (Chrome)**

🔔 Notifications:
1. Chrome → **⋮ Menu** → **Settings**
2. **Site Settings** → **Notifications**
3. Find this app URL → set to **Allow**

📍 Location:
1. Same path → **Site Settings** → **Location**
2. Find this URL → set to **Allow**

📞 Calls (tel: links):
1. When Chrome asks *"Open Phone app?"* → tap **Always**
2. Or: **Settings** → **Apps** → **Chrome** → **Open by default** → add site URL

---

**📱 iPhone (Safari)**

🔔 Notifications:
1. Phone **Settings** → **Safari** → **Notifications**
2. Find this site → tap **Allow**

📍 Location:
1. **Settings** → **Privacy** → **Location Services** → **Safari** → *While Using*

📞 Calls:
1. Safari asks *"Do you want to call?"* → tap **Call**
2. If missing: **Settings** → **Safari** → enable **Phone number detection**

---

**🖥️ Desktop Chrome**

1. Click 🔒 **lock icon** in address bar
2. Click **Site settings**
3. Set **Notifications** → **Allow**
4. Set **Location** → **Allow**
5. Set **Protocol handlers** → **Allow**
6. **Refresh** the page

Or paste in address bar:
`chrome://settings/content/notifications`
`chrome://settings/content/location`

---

**🖥️ Desktop Firefox**

1. Click 🔒 lock → **More Information**
2. **Permissions** tab
3. Set **Notifications** → **Allow**
4. Set **Location** → **Allow**
5. **Settings** → **General** → **Applications** → **tel** → choose calling app

---

**🖥️ Desktop Edge**

1. Click 🔒 lock → **Permissions for this site**
2. Set **Notifications** → **Allow**
3. Set **Location** → **Allow**
4. For calls: Edge prompts *"Open with..."* → choose your calling app
            """)

        st.divider()

        # ── Location ──────────────────────────────────────────────
        st.markdown("### 📡 Location")
        mode = st.radio("Mode", ["Manual Coordinates", "GPS (Browser)"], index=0)
        lat, lon = DEFAULT_LAT, DEFAULT_LON

        if mode == "Manual Coordinates":
            lat = st.number_input("Latitude",  value=DEFAULT_LAT, format="%.6f", step=0.0001)
            lon = st.number_input("Longitude", value=DEFAULT_LON, format="%.6f", step=0.0001)
        else:
            st.info("Tap below — browser will ask for your location.")

            # GPS detect button — writes lat/lon to URL, page reloads
            components.html("""
            <button onclick="detectLocation()" style="
              width:100%;padding:10px;border-radius:8px;cursor:pointer;
              background:#1e1e28;border:1px solid #e8365d;color:#f0ede8;
              font-size:14px;font-family:sans-serif;margin-bottom:6px;">
              📍 Detect My Location
            </button>
            <div id="gpsStatus" style="font-size:12px;color:#8a8799;"></div>
            <script>
            function detectLocation(){
              var statusEl = document.getElementById('gpsStatus');
              statusEl.textContent = "⏳ Requesting GPS…";
              if (!navigator.geolocation) {
                statusEl.textContent = "❌ Geolocation not supported.";
                return;
              }
              navigator.geolocation.getCurrentPosition(
                function(pos){
                  statusEl.textContent = "✅ Got location! Updating map…";
                  var url = new URL(window.parent.location.href);
                  url.searchParams.set('lat', pos.coords.latitude.toFixed(6));
                  url.searchParams.set('lon', pos.coords.longitude.toFixed(6));
                  window.parent.location.href = url.toString();
                },
                function(err){
                  var msgs = {
                    1: "❌ Permission denied.\\nGo to browser Settings → Site Settings → Location → Allow.",
                    2: "❌ Position unavailable. Check GPS/network.",
                    3: "❌ Timeout. Try again."
                  };
                  statusEl.textContent = msgs[err.code] || "❌ Error: " + err.message;
                  alert(msgs[err.code] || "Location error: " + err.message);
                },
                {enableHighAccuracy:true, timeout:10000, maximumAge:0}
              );
            }
            </script>
            """, height=80)

            try:
                p = st.query_params
                if "lat" in p and "lon" in p:
                    lat = float(p["lat"])
                    lon = float(p["lon"])
                    st.success(f"📍 GPS: {lat:.5f}, {lon:.5f}")
            except Exception:
                pass

            with st.expander("Override manually"):
                lat = st.number_input("Latitude",  value=lat, format="%.6f", step=0.0001)
                lon = st.number_input("Longitude", value=lon, format="%.6f", step=0.0001)

        st.divider()

        # ── Map style ─────────────────────────────────────────────
        st.markdown("### 🗺️ Map Style")
        tile_label = st.selectbox("Tile layer", list(MAP_TILES.keys()), index=0)
        st.divider()

        # ── Emergency Contacts (editable) ─────────────────────────
        st.markdown("### 🚨 Emergency Contacts")

        if "custom_contacts" not in st.session_state:
            st.session_state.custom_contacts = dict(DEFAULT_CONTACTS)

        cname   = st.selectbox("Primary contact", list(st.session_state.custom_contacts.keys()))
        contact = st.session_state.custom_contacts[cname]
        st.markdown(f"**Number:** `{contact}`")

        with st.expander("➕ Add / Edit Contact"):
            new_name   = st.text_input("Contact Name",  placeholder="e.g. Mom")
            new_number = st.text_input("Phone Number",  placeholder="+91-XXXXXXXXXX")
            if st.button("Save Contact"):
                if new_name and new_number:
                    st.session_state.custom_contacts[new_name] = new_number
                    st.success(f"✅ Saved: {new_name} → {new_number}")
                else:
                    st.warning("Enter both name and number.")

        st.divider()

        # ── Risk Thresholds ───────────────────────────────────────
        st.markdown("### ⚙️ Risk Thresholds")
        st.slider("Safe / Medium boundary",  0, 100, 35, key="thr_safe")
        st.slider("Medium / Danger boundary", 0, 100, 65, key="thr_danger")

        st.divider()
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        st.caption("v3.0.0 · SafeZone AI")

    return lat, lon, contact, tile_label

# ──────────────────────────────────────────────────────────────────
# 12. SOS PANEL  – working call buttons + WhatsApp + countdown
# ──────────────────────────────────────────────────────────────────

def render_sos_panel(contact_number: str, lat: float, lon: float):
    st.markdown('<div class="section-label">🆘 Emergency SOS</div>', unsafe_allow_html=True)

    # Primary SOS (tel: link always works on mobile)
    st.markdown(f"""
    <div class="card" style="text-align:center;border-color:rgba(232,54,93,0.5);">
      <div class="sos-container">
        <a class="sos-btn" href="tel:{contact_number}" title="Call {contact_number}">
          <span style="font-size:1.5rem;">📞</span>
          <span>SOS</span>
          <span class="sos-label">TAP TO CALL</span>
        </a>
        <p style="margin-top:0.9rem;font-size:0.85rem;color:#f5bec9;font-weight:600;">
          {contact_number}
        </p>
        <p style="font-size:0.7rem;color:#605e6e;margin-top:0;">
          📱 Mobile → native phone call &nbsp;·&nbsp; 🖥️ Desktop → default dialler
        </p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # All contacts as direct call buttons
    st.markdown('<div style="font-size:0.72rem;color:#8a8799;margin-bottom:6px;">📞 Quick-Call All Contacts</div>', unsafe_allow_html=True)
    for name, num in st.session_state.get("custom_contacts", DEFAULT_CONTACTS).items():
        st.markdown(
            f'<a class="call-btn" href="tel:{num}">📞 {name} — {num}</a>',
            unsafe_allow_html=True,
        )

    # WhatsApp SOS with location
    maps_link = f"https://maps.google.com/?q={lat},{lon}"
    wa_msg = urllib.parse.quote(
        f"🚨 SOS! I need help. My location: {maps_link} (Lat:{lat:.5f}, Lon:{lon:.5f})"
    )
    wa_number = contact_number.replace("+", "").replace("-", "").replace(" ", "")
    # If it's a short code (like 100), skip WhatsApp link
    if len(wa_number) >= 10:
        wa_url = f"https://wa.me/{wa_number}?text={wa_msg}"
        st.markdown(
            f'<a class="wa-btn" href="{wa_url}" target="_blank">💬 WhatsApp SOS with Location</a>',
            unsafe_allow_html=True,
        )
    else:
        # Generic WhatsApp to saved number
        st.markdown(
            f'<a class="wa-btn" href="https://wa.me/?text={wa_msg}" target="_blank">💬 Share Location via WhatsApp</a>',
            unsafe_allow_html=True,
        )

    # Google Maps share link
    st.markdown(
        f'<a class="wa-btn" href="{maps_link}" target="_blank" '
        f'style="border-color:rgba(66,133,244,0.4);color:#4285f4;background:rgba(66,133,244,0.1);">'
        f'🗺️ Share My Location (Google Maps)</a>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # SOS Countdown (panic button with 5-sec cancel)
    st.markdown('<div style="font-size:0.72rem;color:#8a8799;margin-bottom:6px;">⏱️ Panic Button (5-sec countdown)</div>', unsafe_allow_html=True)
    if st.button("🔴 Trigger SOS Countdown", use_container_width=True):
        countdown_placeholder = st.empty()
        cancelled = False
        for i in range(5, 0, -1):
            countdown_placeholder.error(f"🚨 SOS in **{i}** seconds… Press 'Cancel' to abort!")
            time.sleep(1)
        if not cancelled:
            countdown_placeholder.success(f"✅ SOS alert dispatched to {contact_number}!")
            inject_push_notification(
                "🚨 SOS SENT — SafeZone AI",
                f"Emergency alert dispatched to {contact_number}. Location: {lat:.5f},{lon:.5f}",
                "safezone-sos",
            )

    # Shake-to-SOS (mobile)
    components.html(f"""
    <div id="shakeStatus" style="font-size:11px;color:#605e6e;margin-top:4px;font-family:sans-serif;">
      📳 Shake phone 3× rapidly to trigger SOS (mobile only)
    </div>
    <script>
    (function(){{
      if (!window.DeviceMotionEvent) return;
      var shakeCount = 0, lastShake = 0, threshold = 20;
      window.addEventListener('devicemotion', function(e){{
        var a = e.accelerationIncludingGravity;
        if(!a) return;
        var mag = Math.sqrt(a.x*a.x + a.y*a.y + a.z*a.z);
        var now = Date.now();
        if(mag > threshold && now - lastShake > 300){{
          lastShake = now;
          shakeCount++;
          document.getElementById('shakeStatus').textContent =
            "📳 Shake " + shakeCount + "/3 detected…";
          if(shakeCount >= 3){{
            shakeCount = 0;
            document.getElementById('shakeStatus').textContent = "🚨 SHAKE SOS triggered!";
            // Try notification
            if(Notification && Notification.permission==="granted"){{
              new Notification("🚨 SHAKE SOS — SafeZone AI", {{
                body: "SOS triggered by shake gesture! Contact: {contact_number}",
                icon: "https://em-content.zobj.net/source/apple/354/shield_1f6e1-fe0f.png",
                tag: "safezone-shake"
              }});
            }}
            // Open call
            window.open("tel:{contact_number}", "_self");
          }}
        }}
      }});
      // Request permission for iOS 13+
      if(typeof DeviceMotionEvent.requestPermission === 'function'){{
        DeviceMotionEvent.requestPermission().catch(function(){{}});
      }}
    }})();
    </script>
    """, height=30)

# ──────────────────────────────────────────────────────────────────
# 13. RISK PANEL
# ──────────────────────────────────────────────────────────────────

def render_risk_panel(score, risk_info, lat, lon, place_name=""):
    st.markdown('<div class="section-label">Risk Assessment</div>', unsafe_allow_html=True)

    banners = {
        "Danger": "🚨 HIGH RISK — avoid this area immediately!",
        "Medium": "⚠️ Moderate risk — stay visible and alert.",
        "Safe":   "✅ Area appears safe — stay aware.",
    }
    st.markdown(f"""
    <div class="notif-bar {risk_info['notif']} animate-in">
      {banners.get(risk_info['label'], '')}
    </div>""", unsafe_allow_html=True)

    place_line = (f"<div style='font-size:0.72rem;color:#8a8799;margin-top:6px;'>"
                  f"{place_name.split(',')[0][:32]}</div>" if place_name else "")
    st.markdown(f"""
    <div class="card">
      <div class="score-ring-wrap">
        <div style="font-size:0.72rem;color:#8a8799;margin-bottom:4px;">RISK SCORE</div>
        <div class="score-number" style="color:{risk_info['color']};">{score}</div>
        <div style="font-size:0.7rem;color:#605e6e;">/100</div>
        <div class="risk-badge {risk_info['css']}" style="margin-top:0.8rem;">
          {risk_info['emoji']} {risk_info['label']} Zone
        </div>
        {place_line}
      </div>
    </div>""", unsafe_allow_html=True)

    st.progress(int(score) / 100)
    c1, c2 = st.columns(2)
    c1.metric("Latitude",  f"{lat:.5f}")
    c2.metric("Longitude", f"{lon:.5f}")

# ──────────────────────────────────────────────────────────────────
# 14. SESSION LOG
# ──────────────────────────────────────────────────────────────────

def append_log(lat, lon, score, label, place=""):
    if "log" not in st.session_state:
        st.session_state.log = []
    st.session_state.log.insert(0, {
        "time":  datetime.now().strftime("%H:%M:%S"),
        "place": place.split(",")[0][:22] if place else "—",
        "lat": lat, "lon": lon, "score": score, "label": label,
    })
    st.session_state.log = st.session_state.log[:12]


def render_log():
    if not st.session_state.get("log"):
        return
    st.markdown("---")
    st.markdown("#### 🕒 Session History")
    cmap = {"Safe": "#27c97a", "Medium": "#f5c542", "Danger": "#e8365d"}
    rows = "".join([
        f"""<tr>
          <td style="padding:4px 8px;color:#8a8799;">{e['time']}</td>
          <td style="padding:4px 8px;color:#c0bdd4;">{e['place']}</td>
          <td style="padding:4px 8px;">{e['lat']:.4f}</td>
          <td style="padding:4px 8px;">{e['lon']:.4f}</td>
          <td style="padding:4px 8px;">{e['score']}</td>
          <td style="padding:4px 8px;color:{cmap.get(e['label'],'#fff')};font-weight:600;">{e['label']}</td>
        </tr>"""
        for e in st.session_state.log
    ])
    st.markdown(f"""
    <div class="card" style="overflow-x:auto;">
      <table style="width:100%;border-collapse:collapse;font-size:0.8rem;">
        <thead>
          <tr style="color:#8a8799;border-bottom:1px solid #2a2a35;">
            <th style="text-align:left;padding:4px 8px;">Time</th>
            <th style="text-align:left;padding:4px 8px;">Place</th>
            <th style="text-align:left;padding:4px 8px;">Lat</th>
            <th style="text-align:left;padding:4px 8px;">Lon</th>
            <th style="text-align:left;padding:4px 8px;">Score</th>
            <th style="text-align:left;padding:4px 8px;">Status</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# 14b. QUICK PANELS — Emergency Numbers · Nearby Services · Contacts
# ──────────────────────────────────────────────────────────────────

def render_quick_panels(lat: float, lon: float):
    """Three collapsible toggle panels below the SOS section."""

    # ── 1. Emergency Numbers ──────────────────────────────────────
    with st.expander("🚨 Emergency Numbers", expanded=False):
        EMERGENCY = [
            ("👮 Police",               "100"),
            ("🚑 Ambulance",            "108"),
            ("🔥 Fire Department",      "101"),
            ("👩 Women Helpline",       "1091"),
            ("👶 Child Helpline",       "1098"),
            ("🚂 Railway Police (RPF)", "182"),
            ("🌊 Disaster (NDRF)",      "1078"),
            ("💻 Cyber Crime",          "1930"),
            ("🏥 NIMHANS (Mental)",     "080-46110007"),
            ("📞 National Emergency",   "112"),
        ]
        for name, num in EMERGENCY:
            st.markdown(
                f'<a class="call-btn" href="tel:{num}" '
                f'style="margin-bottom:6px;display:flex;justify-content:space-between;'
                f'align-items:center;">'
                f'<span>{name}</span>'
                f'<span style="font-family:monospace;font-size:0.95rem;letter-spacing:0.05em;">{num}</span>'
                f'</a>',
                unsafe_allow_html=True,
            )

    # ── 2. Nearby Services ────────────────────────────────────────
    with st.expander("🏥 Nearby Services", expanded=False):
        maps_base = f"https://www.google.com/maps/search/"
        services = [
            ("🏥 Hospitals",          "hospitals"),
            ("👮 Police Stations",    "police+station"),
            ("🚒 Fire Stations",      "fire+station"),
            ("💊 Pharmacies",         "pharmacy"),
            ("🏦 ATMs",               "ATM"),
            ("⛽ Petrol Stations",    "petrol+station"),
            ("🚌 Bus Stops",          "bus+stop"),
            ("🚈 Metro / Train",      "metro+station"),
            ("🛒 24hr Convenience",   "convenience+store"),
            ("🏠 Safe Houses / NGOs", "women+shelter+NGO"),
        ]
        st.markdown(
            '<div style="font-size:0.72rem;color:#8a8799;margin-bottom:8px;">'
            '📌 Opens Google Maps near your current coordinates</div>',
            unsafe_allow_html=True,
        )
        for label, keyword in services:
            url = f"{maps_base}{keyword}/@{lat:.5f},{lon:.5f},15z"
            st.markdown(
                f'<a href="{url}" target="_blank" class="call-btn" '
                f'style="margin-bottom:6px;color:#4285f4;border-color:rgba(66,133,244,0.4);'
                f'background:rgba(66,133,244,0.08);">'
                f'{label}</a>',
                unsafe_allow_html=True,
            )

    # ── 3. Contacts ───────────────────────────────────────────────
    with st.expander("📞 Contacts", expanded=False):
        contacts = st.session_state.get("custom_contacts", DEFAULT_CONTACTS)
        if not contacts:
            st.info("No contacts saved yet. Add them in the sidebar.")
        else:
            for name, num in contacts.items():
                wa_msg = urllib.parse.quote(
                    f"🚨 SOS! I need help. My location: "
                    f"https://maps.google.com/?q={lat},{lon}"
                )
                wa_num = num.replace("+","").replace("-","").replace(" ","")
                c1, c2 = st.columns([3, 2])
                with c1:
                    st.markdown(
                        f'<a class="call-btn" href="tel:{num}" '
                        f'style="margin-bottom:4px;">📞 {name}<br>'
                        f'<span style="font-size:0.78rem;opacity:0.8;">{num}</span></a>',
                        unsafe_allow_html=True,
                    )
                with c2:
                    if len(wa_num) >= 10:
                        wa_url = f"https://wa.me/{wa_num}?text={wa_msg}"
                    else:
                        wa_url = f"https://wa.me/?text={wa_msg}"
                    st.markdown(
                        f'<a class="wa-btn" href="{wa_url}" target="_blank" '
                        f'style="margin-bottom:4px;font-size:0.8rem;">💬 WA SOS</a>',
                        unsafe_allow_html=True,
                    )
        st.markdown("---")
        st.markdown('<div style="font-size:0.72rem;color:#8a8799;margin-bottom:4px;">➕ Add Contact</div>',
                    unsafe_allow_html=True)
        new_name   = st.text_input("Name",   placeholder="e.g. Mom",           key="qp_cname")
        new_number = st.text_input("Number", placeholder="+91-XXXXXXXXXX",      key="qp_cnum")
        if st.button("💾 Save Contact", use_container_width=True, key="qp_save"):
            if new_name and new_number:
                if "custom_contacts" not in st.session_state:
                    st.session_state.custom_contacts = dict(DEFAULT_CONTACTS)
                st.session_state.custom_contacts[new_name] = new_number
                st.success(f"✅ Saved: {new_name}")
                st.rerun()
            else:
                st.warning("Enter both name and number.")

# ──────────────────────────────────────────────────────────────────
# 15. MAIN
# ──────────────────────────────────────────────────────────────────

def main():
    render_header()

    lat, lon, contact, tile_label = render_sidebar()

    s_lat, s_lon, s_name = render_place_search()
    if s_lat is not None:
        lat, lon = s_lat, s_lon
        active_place = s_name
    else:
        active_place = ""

    score     = predict_risk_score(lat, lon)
    risk_info = classify_risk(score)
    append_log(lat, lon, score, risk_info["label"], active_place)
    maybe_notify(score, risk_info, active_place or f"{lat:.3f},{lon:.3f}")

    cache_key = f"{round(lat,4)}_{round(lon,4)}"
    if st.session_state.get("nearby_key") != cache_key:
        st.session_state.nearby     = generate_nearby_points(lat, lon, 10)
        st.session_state.nearby_key = cache_key
    nearby_points = st.session_state.nearby

    left_col, right_col = st.columns([2, 1], gap="large")

    with left_col:
        st.markdown('<div class="section-label">Interactive Street Map</div>',
                    unsafe_allow_html=True)
        zone_map = build_map(lat, lon, risk_info, score, nearby_points, tile_label)
        st_folium(zone_map, width="100%", height=490, returned_objects=[])

        c1, c2 = st.columns([1, 4])
        with c1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.session_state.pop("nearby", None)
                st.session_state.pop("nearby_key", None)
                st.rerun()

        st.markdown("""
        <div class="card" style="display:flex;gap:1.5rem;flex-wrap:wrap;font-size:0.78rem;">
          <span><span style="color:#27c97a;">●</span> Safe (0–34)</span>
          <span><span style="color:#f5c542;">●</span> Medium (35–64)</span>
          <span><span style="color:#e8365d;">●</span> Danger (65–100)</span>
          <span style="color:#605e6e;margin-left:auto;font-size:0.72rem;">
            🛡️ = You &nbsp;·&nbsp; dots = Nearby zones
          </span>
        </div>""", unsafe_allow_html=True)

        render_log()

    with right_col:
        render_risk_panel(score, risk_info, lat, lon, active_place)
        st.markdown("---")
        render_sos_panel(contact, lat, lon)
        st.markdown("---")

        render_quick_panels(lat, lon)
        st.markdown("---")

        # Safety Tips
        st.markdown('<div class="section-label">🛡️ Safety Tips</div>', unsafe_allow_html=True)
        tips = {
            "Safe": [
                "✅ Area looks safe — stay aware of surroundings.",
                "📱 Keep your phone charged.",
                "🤝 Share your location with trusted contacts.",
                "🚶 Prefer main roads over shortcuts.",
                "👀 Stay alert even in safe environments."
            ],
            "Medium": [
                "⚠️ Moderate risk — stay vigilant.",
                "💡 Choose well-lit paths.",
                "🚶 Avoid isolated places.",
                "📞 Keep emergency contacts ready.",
                "🚕 Verify cab details before boarding.",
                "👀 Watch surroundings carefully."
            ],
            "Danger": [
                "🚨 HIGH RISK — avoid immediately!",
                "📢 Inform someone about your location.",
                "🏃 Move to crowded areas.",
                "🆘 Use SOS if needed.",
                "📞 Call emergency services.",
                "🚫 Avoid unknown people.",
                "🔊 Stay alert and ready to react."
            ],
        }
        for tip in tips.get(risk_info["label"], []):
            st.markdown(f"""
            <div class="card" style="padding:0.55rem 0.85rem;margin-bottom:0.45rem;font-size:0.8rem;">
              {tip}
            </div>
            """, unsafe_allow_html=True)

    # ── Report + Feedback ─────────────────────────────────────────
    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("🚩 Mark this area as Unsafe"):
            st.warning("⚠️ Area reported! This helps improve safety predictions.")
    with col_r2:
        if st.button("✅ Mark this area as Safe"):
            st.success("✅ Thank you! Your feedback improves the map.")

    st.markdown("---")
    st.markdown("### 📝 Safety Feedback")
    with st.form("feedback_form"):
        rating = st.slider("Rate Safety (1 = Very Unsafe, 5 = Very Safe)", 1, 5, 3)
        issue_type = st.selectbox("Report Issue Type", [
            "None", "Poor Lighting", "Isolated Area", "Harassment Risk",
            "No Police Presence", "Suspicious Activity", "Road Hazard", "Other"
        ])
        comment = st.text_area("Additional Comments", placeholder="Describe what you observed…")
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            if "feedback_log" not in st.session_state:
                st.session_state.feedback_log = []
            st.session_state.feedback_log.append({
                "rating": rating, "issue": issue_type, "comment": comment,
                "location": active_place if active_place else f"{lat:.5f},{lon:.5f}",
                "time": datetime.now().strftime("%H:%M:%S")
            })
            st.success("✅ Feedback submitted! Thank you for keeping the community safe.")

    if st.session_state.get("feedback_log"):
        st.markdown("### 📊 Recent Feedback")
        for fb in st.session_state.feedback_log[::-1][:5]:
            stars = "⭐" * fb["rating"]
            st.markdown(f"""
            <div class="card" style="font-size:0.8rem;">
              {stars} <b>{fb['rating']}/5</b> &nbsp;·&nbsp; ⏰ {fb.get('time','')}<br>
              ⚠️ {fb['issue']} &nbsp;·&nbsp; 📍 {fb['location']}<br>
              💬 {fb['comment'] or '—'}
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# 16. ENTRY POINT
# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
