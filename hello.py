import streamlit as st
import streamlit.components.v1 as components
import time
import random

# --- PAGE SETUP ---
st.set_page_config(page_title="ASCEND Professional Dashboard", layout="wide")

# --- HARDWARE DATA MAPPING ---
# Replace the 'random' functions with your Serial/WiFi data reading logic
def get_hardware_feed():
    return {
        "fsr_grip": random.uniform(10, 85),     # Grip Force from Interlink FSR (N)
        "servo_height": random.randint(750, 900), # Height from DS3225 (mm)
        "teensy_v": random.uniform(11.5, 12.6), # Battery from Teensy Divider (V)
        "stability": random.uniform(0.02, 0.15),# BNO055 Stability Index
        "dist_curr": random.uniform(15.5, 45.0),# Therapy Distance Progress (m)
        "dist_target": 50,                      # Therapy Goal (m)
        "temp": random.uniform(32, 38)          # Motor/BMS Temperature
    }

# --- STREAMLIT DASHBOARD LOOP ---
placeholder = st.empty()

while True:
    data = get_hardware_feed()
    
    # Calculate Percentages
    batt_pct = max(0, min(100, ((data['teensy_v'] - 10.5) / (12.6 - 10.5)) * 100))
    ex_pct = min(100, (data['dist_curr'] / data['dist_target']) * 100)
    
    # MASTER HTML TEMPLATE
    dashboard_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: 'Inter', sans-serif; background-color: #f3f4f6; padding: 10px; }}
            .card {{ background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); padding: 16px; margin-bottom: 16px; }}
            .tab-btn {{ padding: 12px; flex: 1; text-align: center; cursor: pointer; border-bottom: 2px solid transparent; font-size: 0.875rem; color: #6b7280; }}
            .tab-btn.active {{ border-color: #4f46e5; color: #4f46e5; font-weight: 600; }}
            .tab-content {{ display: none; padding-top: 16px; }}
            .tab-content.active {{ display: block; }}
        </style>
    </head>
    <body>
        <div class="max-w-7xl mx-auto grid grid-cols-12 gap-4">
            
            <div class="col-span-3">
                <div class="card">
                    <h2 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4">Live Vitals</h2>
                    <div class="space-y-3">
                        <div class="bg-indigo-50 p-3 rounded-lg border border-indigo-100">
                            <span class="text-[10px] text-indigo-500 block mb-1">FSR Grip Strength</span>
                            <span class="text-xl font-bold text-indigo-700">{data['fsr_grip']:.1f} <span class="text-xs">N</span></span>
                        </div>
                        <div class="bg-gray-50 p-3 rounded-lg border border-gray-100">
                            <div class="flex justify-between items-center mb-1">
                                <span class="text-[10px] text-gray-500">Battery Level</span>
                                <span class="text-xs font-bold text-gray-700">{batt_pct:.0f}%</span>
                            </div>
                            <span class="text-xl font-bold text-gray-800">{data['teensy_v']:.2f}V</span>
                            <div class="w-full bg-gray-200 h-1.5 rounded-full mt-2">
                                <div class="bg-green-500 h-1.5 rounded-full" style="width: {batt_pct}%"></div>
                            </div>
                        </div>
                        <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg border border-gray-100">
                            <span class="text-xs text-gray-500">Walker Height</span>
                            <span class="text-sm font-bold text-gray-700">{data['servo_height']} mm</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-span-9">
                <div class="bg-white rounded-xl shadow-sm flex overflow-hidden border-b">
                    <div id="tab-controls" class="tab-btn active" onclick="switchTab('controls')">🎮 Controls</div>
                    <div id="tab-therapy" class="tab-btn" onclick="switchTab('therapy')">🏆 Therapy</div>
                    <div id="tab-health" class="tab-btn" onclick="switchTab('health')">🔧 Health</div>
                </div>

                <div class="card mt-4 min-h-[350px]">
                    
                    <div id="content-controls" class="tab-content active">
                        <div class="grid grid-cols-2 gap-3">
                            <button class="col-span-2 py-4 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700">▶ Start Walker Assistance</button>
                            <button class="py-3 bg-red-600 text-white font-semibold rounded-lg">⏹ Emergency Stop</button>
                            <button class="py-3 bg-yellow-500 text-white font-semibold rounded-lg">⚠️ Reset System</button>
                        </div>
                    </div>

                    <div id="content-therapy" class="tab-content">
                        <div class="bg-gradient-to-r from-pink-50 to-purple-50 p-5 rounded-xl border border-pink-100 mb-6">
                            <h3 class="text-lg font-bold text-gray-800">Daily Therapy Progress</h3>
                            <div class="flex justify-between items-center mt-2">
                                <span class="text-sm font-semibold text-gray-600">Goal Progress</span>
                                <span class="text-sm font-bold text-pink-600">{data['dist_curr']:.1f}m / {data['dist_target']}m</span>
                            </div>
                            <div class="w-full bg-white rounded-full h-4 mt-2 relative shadow-inner overflow-hidden">
                                <div class="bg-pink-500 h-4 rounded-full transition-all duration-500" style="width: {ex_pct}%"></div>
                            </div>
                        </div>

                        <h3 class="text-xs font-bold text-gray-400 uppercase mb-3">Badges & Milestones</h3>
                        <div class="grid grid-cols-3 gap-3 text-center">
                            <div class="p-4 bg-gray-50 rounded-lg border border-gray-100">
                                <div class="text-2xl mb-1">🔥</div>
                                <div class="text-xs font-bold text-gray-700">7 Day Streak</div>
                            </div>
                            <div class="p-4 bg-gray-50 rounded-lg border border-gray-100 opacity-40 grayscale">
                                <div class="text-2xl mb-1">🏃</div>
                                <div class="text-xs font-bold text-gray-400">Marathoner</div>
                            </div>
                            <div class="p-4 bg-gray-50 rounded-lg border border-gray-100">
                                <div class="text-2xl mb-1">🛡️</div>
                                <div class="text-xs font-bold text-gray-700">Fall Free</div>
                            </div>
                        </div>
                    </div>

                    <div id="content-health" class="tab-content">
                        <div class="grid grid-cols-2 gap-4">
                            <div class="p-4 bg-gray-50 rounded-xl border border-gray-100">
                                <span class="text-xs text-gray-500 uppercase">Motor Temperature</span>
                                <div class="flex items-center gap-2 mt-1">
                                    <span class="text-2xl font-bold text-gray-800">{data['temp']:.1f}°C</span>
                                    <span class="text-[10px] font-bold text-green-600 bg-green-100 px-1.5 py-0.5 rounded">OK</span>
                                </div>
                            </div>
                            <div class="p-4 bg-gray-50 rounded-xl border border-gray-100">
                                <span class="text-xs text-gray-500 uppercase">System Stability</span>
                                <div class="mt-1">
                                    <span class="text-2xl font-bold text-gray-800">{data['stability']:.2f}</span>
                                    <span class="text-[10px] text-gray-400 ml-1">Normal range</span>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <script>
            function switchTab(id) {{
                document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
                document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
                document.getElementById('content-' + id).classList.add('active');
                document.getElementById('tab-' + id).classList.add('active');
            }}
        </script>
    </body>
    </html>
    """
    
    with placeholder:
        components.html(dashboard_html, height=600)
    
    time.sleep(0.5)
