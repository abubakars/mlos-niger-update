with st.sidebar.form("add_data_form"):
    st.markdown("### ➕ Add New Entry")

    # Location group
    with st.expander("📍 Location Info"):
        state_name = st.text_input("State")
        lga_name = st.text_input("LGA")
        ward_name = st.text_input("Ward")
        ward_code = st.text_input("Ward Code")
        take_off_point = st.text_input("Take-off Point")
        takeoffpoint_code = st.text_input("Take-off Code")

    # Settlement info
    with st.expander("🧭 Settlement Info"):
        chn = st.text_input("CHN")
        settlement_name = st.text_input("Settlement Name")
        primary_settlement_name = st.text_input("Primary Settlement Name")
        alternate_name = st.text_input("Alternate Name")
        health_facility = st.text_input("RI Health Facility")
        latitude = st.number_input("Latitude", format="%.6f")
        longitude = st.number_input("Longitude", format="%.6f")

    # Status and conditions
    with st.expander("📌 Accessibility & Status"):
        conc = st.selectbox("Conc", ["Yes", "No"])
        duplicate = st.selectbox("Duplicate", ["Yes", "No"])
        status = st.selectbox("Status", ["Accessible", "Inaccessible"])
        security_compromised = st.selectbox("Security Compromised", ["Yes", "No"])
        accessibility_status = st.text_input("Accessibility Status")
        reasons_for_inaccessibility = st.text_input("Reason for Inaccessibility")
        habitational_status = st.text_input("Habitational Status")

    # Demographics
    with st.expander("👥 Population Info"):
        set_population = st.number_input("Set Population", step=1)
        set_target = st.number_input("Set Target", step=1)
        number_of_household = st.number_input("No. of Households", step=1)
        noncompliant_household = st.number_input("Noncompliant Households", step=1)

    # Activity
    with st.expander("📅 Activity"):
        team_code = st.text_input("Team Code")
        day_of_activity = st.date_input("Date of Activity", format="DD/MM/YYYY")

    # Tags
    with st.expander("🗺️ Tags"):
        urban = st.checkbox("Urban")
        rural = st.checkbox("Rural")
        scattered = st.checkbox("Scattered")
        highrisk = st.checkbox("High Risk")
        slums = st.checkbox("Slums")
        densely_populated = st.checkbox("Densely Populated")
        hard2reach = st.checkbox("Hard-to-Reach")
        border = st.checkbox("Border")
        nomadic = st.checkbox("Nomadic")
        riverine = st.checkbox("Riverine")
        fulani = st.checkbox("Fulani")

    submitted = st.form_submit_button("Add Entry")
if submitted:
    new_row = {
        "state_name": state_name,
        "lga_name": lga_name,
        "ward_name": ward_name,
        "ward_code": ward_code,
        "take_off_point": take_off_point,
        "takeoffpoint_code": takeoffpoint_code,
        "chn": chn,
        "settlement_name": settlement_name,
        "primary_settlement_name": primary_settlement_name,
        "alternate_name": alternate_name,
        "name of RI Health Facility": health_facility,
        "latitude": latitude,
        "longitude": longitude,
        "conc": conc,
        "Duplicate": duplicate,
        "status": status,
        "security_compromised": security_compromised,
        "accessibility_status": accessibility_status,
        "reasons_for_inaccessibility": reasons_for_inaccessibility,
        "habitational_status": habitational_status,
        "set_population": set_population,
        "set_target": set_target,
        "number_of_household": number_of_household,
        "noncompliant_household": noncompliant_household,
        "team_code": team_code,
        "day_of_activity": day_of_activity.strftime("%d/%m/%Y"),
        "urban": urban,
        "rural": rural,
        "scattered": scattered,
        "highrisk": highrisk,
        "slums": slums,
        "densely_populated": densely_populated,
        "hard2reach": hard2reach,
        "border": border,
        "nomadic": nomadic,
        "riverine": riverine,
        "fulani": fulani
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    st.success("✅ New entry added!")
