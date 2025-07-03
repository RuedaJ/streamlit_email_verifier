import streamlit as st
import pandas as pd
import requests

st.title("📧 Email Verification Tool (Mailboxlayer + NeverBounce Ready)")

# Upload a CSV file
uploaded_file = st.file_uploader("Upload your contact CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "Email" not in df.columns:
        st.error("The uploaded file must have an 'Email' column.")
    else:
        mailboxlayer_key = st.secrets["api_keys"]["mailboxlayer"]
        # neverbounce_key = st.secrets["api_keys"]["neverbounce"]  # Uncomment when ready

        verified_emails = []

        for email in df["Email"]:
            email = str(email).strip()
            if not email or "@" not in email:
                verified_emails.append("Invalid format")
                continue

            # Validate using Mailboxlayer
            mb_url = f"http://apilayer.net/api/check?access_key={mailboxlayer_key}&email={email}&smtp=1&format=1"
            response = requests.get(mb_url)
            if response.status_code == 200:
                data = response.json()
                if data.get("format_valid") and data.get("smtp_check"):
                    verified_emails.append("Valid (Mailboxlayer)")
                else:
                    verified_emails.append("Invalid (Mailboxlayer)")
            else:
                verified_emails.append("Error checking")

            # Optional: Add Neverbounce check (commented)
            # nb_url = f"https://api.neverbounce.com/v4/single/check?key={neverbounce_key}&email={email}"
            # nb_response = requests.get(nb_url)
            # if nb_response.status_code == 200:
            #     nb_data = nb_response.json()
            #     if nb_data["result"] == "valid":
            #         verified_emails.append("Valid (Neverbounce)")
            #     else:
            #         verified_emails.append(f"{nb_data['result'].capitalize()} (Neverbounce)")
            # else:
            #     verified_emails.append("Error (Neverbounce)")

        df["Email Validity"] = verified_emails

        st.success("✅ Verification complete!")
        st.dataframe(df)

        st.download_button("📥 Download Verified CSV", data=df.to_csv(index=False), file_name="verified_contacts.csv", mime="text/csv")
