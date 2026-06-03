import streamlit as st
import numpy as np
from simulator_engine import kingshot_multirally_sim2, TroopSide, load_hero_db

# =========================================================================
# --- SECURITY GATEWAY ---
# =========================================================================
SECRET_PASSCODE = "Frank_BattleSimulator"

st.set_page_config(page_title="Kingshot Simulator", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Security Access Required")
    user_input = st.text_input("Enter Alliance Passcode:", type="password")
    
    if st.button("Unlock Simulator"):
        if user_input == SECRET_PASSCODE:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid passcode. Access denied.")
else:
    # =========================================================================
    # --- SIMULATOR APPLICATION (UNLOCKED) ---
    # =========================================================================
    st.title("⚔️ Kingshot Single Rally & Garrison Simulator")
    
    
    if st.sidebar.button("Lock Application"):
        st.session_state["authenticated"] = False
        st.rerun()

    # Pull all available hero names directly from your existing database
    hero_list = sorted(list(load_hero_db().keys()))

    col1, col2 = st.columns(2)
    
    # -------------------------------------------------------------------------
    # --- GARRISON SIDE CONFIG ---
    # -------------------------------------------------------------------------
    with col1:
        st.header("🏰 Garrison Defense Setup")
        g_inf = st.number_input("Garrison Infantry Count", value=582873)
        g_cav = st.number_input("Garrison Cavalry Count", value=174733)
        g_arc = st.number_input("Garrison Archer Count", value=322047)
        
        st.markdown("**Garrison Tier-10 (TG3) Ratios**")
        g_ratio_inf = st.slider("Garrison Infantry TG3 %", 0.0, 1.0, 1.0)
        g_ratio_cav = st.slider("Garrison Cavalry TG3 %", 0.0, 1.0, 1.0)
        g_ratio_arc = st.slider("Garrison Archer TG3 %", 0.0, 1.0, 1.0)
        
        # --- Garrison Hero Dropdowns ---
        with st.expander("🎖️ Garrison Hero Lineup Selection"):
            st.markdown("##### 👑 Garrison Leaders (Up to 3)")
            g_lead1 = st.selectbox("Garrison Leader 1", hero_list, index=hero_list.index("Amadeus") if "Amadeus" in hero_list else 0)
            g_lead2 = st.selectbox("Garrison Leader 2", hero_list, index=hero_list.index("Hilde") if "Hilde" in hero_list else 0)
            g_lead3 = st.selectbox("Garrison Leader 3", hero_list, index=hero_list.index("Marlin") if "Marlin" in hero_list else 0)
            
            st.markdown("##### 👥 Garrison Supporters (4 Reinforcers)")
            g_sup1 = st.selectbox("Garrison Supporter 1", hero_list, index=hero_list.index("Gordon") if "Gordon" in hero_list else 0)
            g_sup2 = st.selectbox("Garrison Supporter 2", hero_list, index=hero_list.index("Gordon") if "Gordon" in hero_list else 0)
            g_sup3 = st.selectbox("Garrison Supporter 3", hero_list, index=hero_list.index("Gordon") if "Gordon" in hero_list else 0)
            g_sup4 = st.selectbox("Garrison Supporter 4", hero_list, index=hero_list.index("Gordon") if "Gordon" in hero_list else 0)
        
        with st.expander("📊 Edit Garrison Combat Stats (12 Variables)"):
            st.markdown("##### 🛡️ Infantry Stats")
            g_inf_atk = st.number_input("Garrison Infantry Attack %", value=858.7)
            g_inf_def = st.number_input("Garrison Infantry Defense %", value=909.9)
            g_inf_let = st.number_input("Garrison Infantry Lethality %", value=1182.5)
            g_inf_hp  = st.number_input("Garrison Infantry Health %", value=1182.5)
            
            st.markdown("##### 🐴 Cavalry Stats")
            g_cav_atk = st.number_input("Garrison Cavalry Attack %", value=813.7)
            g_cav_def = st.number_input("Garrison Cavalry Defense %", value=801.4)
            g_cav_let = st.number_input("Garrison Cavalry Lethality %", value=1039.5)
            g_cav_hp  = st.number_input("Garrison Cavalry Health %", value=1007.3)
            
            st.markdown("##### 🏹 Archer Stats")
            g_arc_atk = st.number_input("Garrison Archer Attack %", value=850.2)
            g_arc_def = st.number_input("Garrison Archer Defense %", value=823.4)
            g_arc_let = st.number_input("Garrison Archer Lethality %", value=1126.7)
            g_arc_hp  = st.number_input("Garrison Archer Health %", value=1088.4)

    # -------------------------------------------------------------------------
    # --- ATTACKER SIDE CONFIG ---
    # -------------------------------------------------------------------------
    with col2:
        st.header("🚀 Attacker Rally Setup")
        a_inf = st.number_input("Attacker Infantry Count", value=580373)
        a_cav = st.number_input("Attacker Cavalry Count", value=279146)
        a_arc = st.number_input("Attacker Archer Count", value=225733)
        
        st.markdown("**Attacker Tier-10 (TG3) Purity Ratios**")
        a_ratio_inf = st.slider("Attacker Infantry TG3 %", 0.0, 1.0, 1.0)
        a_ratio_cav = st.slider("Attacker Cavalry TG3 %", 0.0, 1.0, 1.0)
        a_ratio_arc = st.slider("Attacker Archer TG3 %", 0.0, 1.0, 1.0)
        
        # --- Attacker Hero Dropdowns ---
        with st.expander("🎖️ Attacker Hero Lineup Selection"):
            st.markdown("##### 👑 Rally Leaders (Up to 3)")
            a_lead1 = st.selectbox("Rally Leader 1", hero_list, index=hero_list.index("Amadeus") if "Amadeus" in hero_list else 0)
            a_lead2 = st.selectbox("Rally Leader 2", hero_list, index=hero_list.index("Marlin") if "Marlin" in hero_list else 0)
            a_lead3 = st.selectbox("Rally Leader 3", hero_list, index=hero_list.index("Petra") if "Petra" in hero_list else 0)
            
            st.markdown("##### 👥 Rally Joiners (4 Supporters)")
            a_sup1 = st.selectbox("Rally Joiner 1", hero_list, index=hero_list.index("Chenko") if "Chenko" in hero_list else 0)
            a_sup2 = st.selectbox("Rally Joiner 2", hero_list, index=hero_list.index("Chenko") if "Chenko" in hero_list else 0)
            a_sup3 = st.selectbox("Rally Joiner 3", hero_list, index=hero_list.index("Chenko") if "Chenko" in hero_list else 0)
            a_sup4 = st.selectbox("Rally Joiner 4", hero_list, index=hero_list.index("Chenko") if "Chenko" in hero_list else 0)
        
        with st.expander("📊 Edit Attacker Combat Stats (12 Variables)"):
            st.markdown("##### 🛡️ Infantry Stats")
            a_inf_atk = st.number_input("Attacker Infantry Attack %", value=1031.8)
            a_inf_def = st.number_input("Attacker Infantry Defense %", value=781.2)
            a_inf_let = st.number_input("Attacker Infantry Lethality %", value=1147.8)
            a_inf_hp  = st.number_input("Attacker Infantry Health %", value=903.8)
            
            st.markdown("##### 🐴 Cavalry Stats")
            a_cav_atk = st.number_input("Attacker Cavalry Attack %", value=948.5)
            a_cav_def = st.number_input("Attacker Cavalry Defense %", value=747.1)
            a_cav_let = st.number_input("Attacker Cavalry Lethality %", value=869.2)
            a_cav_hp  = st.number_input("Attacker Cavalry Health %", value=688.7)
            
            st.markdown("##### 🏹 Archer Stats")
            a_arc_atk = st.number_input("Attacker Archer Attack %", value=925.5)
            a_arc_def = st.number_input("Attacker Archer Defense %", value=706.6)
            a_arc_let = st.number_input("Attacker Archer Lethality %", value=1050.4)
            a_arc_hp  = st.number_input("Attacker Archer Health %", value=822.7)

    st.markdown("---")
    num_runs = st.number_input("Monte Carlo Simulation Runs", min_value=10, max_value=1000, value=500, step=50)

    # =========================================================================
    # --- EXECUTION ENGINE ---
    # =========================================================================
    if st.button("🚀 Execute Strategic Analysis"):
        with st.spinner("Processing tactical parameters..."):
            
            # Pack live front-end inputs dynamically into the 3x4 layout matrices
            g_stats = [
                [g_inf_atk, g_inf_def, g_inf_let, g_inf_hp],
                [g_cav_atk, g_cav_def, g_cav_let, g_cav_hp],
                [g_arc_atk, g_arc_def, g_arc_let, g_arc_hp]
            ]
            
            g_leaders = [g_lead1, g_lead2, g_lead3]
            g_supporters = [g_sup1, g_sup2, g_sup3, g_sup4]
            
            garrison_setup = TroopSide(
                troops=[g_inf, g_cav, g_arc], 
                stats=g_stats, 
                leader_heroes=g_leaders,
                supporter_heroes=g_supporters,
                tg3_ratio=[g_ratio_inf, g_ratio_cav, g_ratio_arc]
            )
            
            w1_stats = [
                [a_inf_atk, a_inf_def, a_inf_let, a_inf_hp],
                [a_cav_atk, a_cav_def, a_cav_let, a_cav_hp],
                [a_arc_atk, a_arc_def, a_arc_let, a_arc_hp]
            ]
            
            a_leaders = [a_lead1, a_lead2, a_lead3]
            a_supporters = [a_sup1, a_sup2, a_sup3, a_sup4]
            
            wave1_setup = TroopSide(
                troops=[a_inf, a_cav, a_arc],
                stats=w1_stats,
                leader_heroes=a_leaders,
                supporter_heroes=a_supporters,
                tg3_ratio=[a_ratio_inf, a_ratio_cav, a_ratio_arc]
            )
            
            rally_waves_input = [wave1_setup]
            
            # --- MONTE CARLO PROCESSING WITH TRACKING FOR BOTH SIDES ---
            d_surviving_sum = 0
            d_surviving_array = np.zeros(3)
            d_worst = float('inf')
            d_best = 0.0
            
            a_surviving_sum = 0
            a_surviving_array = np.zeros(3)
            a_worst = float('inf')
            a_best = 0.0
            
            for _ in range(int(num_runs)):
                final_garrison, logs = kingshot_multirally_sim2(rally_waves_input, garrison_setup)
                
                # Defender tracking
                d_run_survivors = final_garrison.troops
                d_run_total = np.sum(d_run_survivors)
                d_surviving_array += d_run_survivors
                d_surviving_sum += d_run_total
                if d_run_total < d_worst: d_worst = d_run_total
                if d_run_total > d_best: d_best = d_run_total
                
                # Attacker tracking (grabs the remaining troops from the last wave processed)
                a_run_survivors = logs[-1]['attacker_surviving']
                a_run_total = np.sum(a_run_survivors)
                a_surviving_array += a_run_survivors
                a_surviving_sum += a_run_total
                if a_run_total < a_worst: a_worst = a_run_total
                if a_run_total > a_best: a_best = a_run_total
                
            # Compute averages
            d_avg_array = d_surviving_array / num_runs
            d_avg_sum = d_surviving_sum / num_runs
            
            a_avg_array = a_surviving_array / num_runs
            a_avg_sum = a_surviving_sum / num_runs
            
            # --- WEB INTERFACE LAYOUT DISPLAY ---
            st.success("Simulation Complete!")
            
            # Base logic to figure out overall match leaning
            if d_avg_sum > a_avg_sum:
                victory_title = "🏰 GARRISON DEFENSE LEANING"
                status_color = "green"
            else:
                victory_title = "🚀 ATTACKER RALLY LEANING"
                status_color = "red"
                
            st.markdown("### <span style='color:" + status_color + "'>" + victory_title + "</span>", unsafe_allow_html=True)
            
            # Side-by-Side Metric Spread
            out_col1, out_col2 = st.columns(2)
            
            with out_col1:
                st.markdown("#### 🏰 Defender Spread Metrics")
                st.metric("Avg Garrison Survivors", f"{d_avg_sum:,.0f}")
                st.metric("Garrison Worst Case", f"{d_worst:,.0f}")
                st.metric("Garrison Best Case", f"{d_best:,.0f}")
                
                st.markdown("##### 📊 Avg Remaining Garrison Breakdown")
                st.table({
                    "Troop Class": ["🛡️ Infantry frontline", "🐴 Cavalry flanking", "🏹 Archer backend"],
                    "Surviving": [f"{d_avg_array[0]:,.0f}", f"{d_avg_array[1]:,.0f}", f"{d_avg_array[2]:,.0f}"]
                })
                
            with out_col2:
                st.markdown("#### 🚀 Attacker Spread Metrics")
                st.metric("Avg Attacker Survivors", f"{a_avg_sum:,.0f}")
                st.metric("Attacker Worst Case", f"{a_worst:,.0f}")
                st.metric("Attacker Best Case", f"{a_best:,.0f}")
                
                st.markdown("##### 📊 Avg Remaining Attacker Breakdown")
                st.table({
                    "Troop Class": ["🛡️ Infantry frontline", "🐴 Cavalry flanking", "🏹 Archer backend"],
                    "Surviving": [f"{a_avg_array[0]:,.0f}", f"{a_avg_array[1]:,.0f}", f"{a_avg_array[2]:,.0f}"]
                })