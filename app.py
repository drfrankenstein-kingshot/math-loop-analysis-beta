import streamlit as st
import numpy as np
from simulator_engine import kingshot_multirally_sim2, TroopSide

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
    st.title("⚔️ Kingshot Multi-Rally & Garrison Simulator")
    st.subheader("State of Survival Hidden Core Architecture Engine")
    
    if st.sidebar.button("Lock Application"):
        st.session_state["authenticated"] = False
        st.rerun()

    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🏰 Garrison Defense Setup")
        g_inf = st.number_input("Garrison Infantry Count", value=582873)
        g_cav = st.number_input("Garrison Cavalry Count", value=174733)
        g_arc = st.number_input("Garrison Archer Count", value=322047)
        
        st.markdown("**Garrison Tier-10 (TG3) Purity Ratios**")
        g_ratio_inf = st.slider("Garrison Infantry TG3 %", 0.0, 1.0, 1.0)
        g_ratio_cav = st.slider("Garrison Cavalry TG3 %", 0.0, 1.0, 1.0)
        g_ratio_arc = st.slider("Garrison Archer TG3 %", 0.0, 1.0, 1.0)

    with col2:
        st.header("🚀 Attacker Rally Setup")
        a_inf = st.number_input("Attacker Infantry Count", value=580373)
        a_cav = st.number_input("Attacker Cavalry Count", value=279146)
        a_arc = st.number_input("Attacker Archer Count", value=225733)
        
        st.markdown("**Attacker Tier-10 (TG3) Purity Ratios**")
        a_ratio_inf = st.slider("Attacker Infantry TG3 %", 0.0, 1.0, 1.0)
        a_ratio_cav = st.slider("Attacker Cavalry TG3 %", 0.0, 1.0, 1.0)
        a_ratio_arc = st.slider("Attacker Archer TG3 %", 0.0, 1.0, 1.0)

    st.markdown("---")
    num_runs = st.number_input("Monte Carlo Simulation Runs", min_value=10, max_value=1000, value=500, step=50)

    if st.button("🚀 Execute Strategic Analysis"):
        with st.spinner("Processing tactical parameters..."):
            
            # Reconstruct the precise testing parameters from your wrapper script
            g_stats = [
                [858.7, 909.9, 1182.5, 1182.5],
                [813.7, 801.4, 1039.5, 1007.3],
                [850.2, 823.4, 1126.7, 1088.4]
            ]
            garrison_setup = TroopSide(
                troops=[g_inf, g_cav, g_arc], 
                stats=g_stats, 
                leader_heroes=["Amadeus", "Hilde", "Marlin"],
                supporter_heroes=["Gordon", "Gordon", "Gordon", "Gordon"],
                tg3_ratio=[g_ratio_inf, g_ratio_cav, g_ratio_arc]
            )
            
            w1_stats = [
                [1031.8, 781.2, 1147.8, 903.8],
                [948.5,  747.1, 869.2,  688.7],
                [925.5,  706.6, 1050.4, 822.7]
            ]
            wave1_setup = TroopSide(
                troops=[a_inf, a_cav, a_arc],
                stats=w1_stats,
                leader_heroes=["Amadeus", "Marlin", "Petra"],
                supporter_heroes=["Chenko", "Chenko", "Chenko", "Chenko"],
                tg3_ratio=[a_ratio_inf, a_ratio_cav, a_ratio_arc]
            )
            
            rally_waves_input = [wave1_setup]
            
            # Running the Monte Carlo Loop
            total_surviving_sum = 0
            total_surviving_array = np.zeros(3)
            worst_case = float('inf')
            best_case = 0.0
            
            for _ in range(int(num_runs)):
                final_garrison, logs = kingshot_multirally_sim2(rally_waves_input, garrison_setup)
                run_survivors = final_garrison.troops
                run_total = np.sum(run_survivors)
                
                total_surviving_array += run_survivors
                total_surviving_sum += run_total
                
                if run_total < worst_case: worst_case = run_total
                if run_total > best_case: best_case = run_total
                
            avg_surviving_array = total_surviving_array / num_runs
            avg_surviving_sum = total_surviving_sum / num_runs
            
            # --- WEB INTERFACE LAYOUT DISPLAY ---
            st.success("Simulation Complete!")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Average Total Survivors", f"{avg_surviving_sum:,.0f}")
            m2.metric("Worst Case Scenario", f"{worst_case:,.0f}")
            m3.metric("Best Case Scenario", f"{best_case:,.0f}")
            
            st.markdown("### 📊 Troop Class Survival Proportions")
            st.table({
                "Troop Class Type": ["🛡️ Infantry frontline", "🐴 Cavalry flanking", "🏹 Archer backend"],
                "Average Surviving Units": [f"{avg_surviving_array[0]:,.0f}", f"{avg_surviving_array[1]:,.0f}", f"{avg_surviving_array[2]:,.0f}"]
            })