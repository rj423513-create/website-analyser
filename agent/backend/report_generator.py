import pandas as pd

def generate_excel_report(df_all_domain, df_all_pages, df_all_issues, df_all_audit, filename):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_all_domain.to_excel(
            writer, sheet_name='Domain_Info', index=False)
        df_all_pages.to_excel(
            writer, sheet_name='Crawled_Pages', index=False)
        if not df_all_issues.empty:
            df_all_issues.to_excel(
                writer, sheet_name='SEO_Issues', index=False)
        if not df_all_audit.empty:
            df_all_audit.to_excel(
                writer, sheet_name='Technical_Audit', index=False)
