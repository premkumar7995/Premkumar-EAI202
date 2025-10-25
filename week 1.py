# =============================
# FIFA WORLD CUP DATA CLEANING
# matches_1930_2022.xlsx
# =============================

import pandas as pd, re
from google.colab import files
from io import BytesIO

# 1️⃣ Upload Excel file
print("📂 Upload your matches_1930_2022.xlsx file")
uploaded = files.upload()
filename = list(uploaded.keys())[0]
df = pd.read_excel(BytesIO(uploaded[filename]))
print("✅ File loaded:", filename, "Rows:", len(df))

# 2️⃣ Remove duplicates
df.drop_duplicates(inplace=True)

# 3️⃣ Standardize column names
df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('[^a-z0-9_]', '', regex=True))

# 4️⃣ Fill missing values
for c in df.columns:
    if df[c].dtype == 'object':
        df[c] = df[c].fillna('Unknown').str.strip()
    else:
        df[c] = df[c].fillna(0)

# 5️⃣ Normalize text columns
for c in df.select_dtypes(include='object').columns:
    df[c] = df[c].astype(str).str.title().str.strip()

# 6️⃣ Parse score column if present
if 'score' in df.columns and ('home_team_goals' not in df.columns):
    def split_score(s):
        if pd.isna(s): return (0,0)
        m = re.search(r'(\d+)\D+(\d+)', str(s))
        return (int(m.group(1)), int(m.group(2))) if m else (0,0)
    df[['home_team_goals','away_team_goals']] = df['score'].apply(split_score).tolist()

# 7️⃣ Compute goal difference & winning team
if {'home_team_goals','away_team_goals'}.issubset(df.columns):
    df['home_team_goals'] = pd.to_numeric(df['home_team_goals'], errors='coerce').fillna(0).astype(int)
    df['away_team_goals'] = pd.to_numeric(df['away_team_goals'], errors='coerce').fillna(0).astype(int)
    df['goal_difference'] = abs(df['home_team_goals'] - df['away_team_goals'])
    def winner(r):
        if r['home_team_goals'] > r['away_team_goals']: return r.get('home_team','Unknown')
        if r['away_team_goals'] > r['home_team_goals']: return r.get('away_team','Unknown')
        return 'Draw'
    df['winning_team'] = df.apply(winner, axis=1)

# 8️⃣ Sort by year/date if available
for col in ['year','date','match_date']:
    if col in df.columns:
        df.sort_values(by=col, inplace=True)
        break

# 9️⃣ Re-order main columns for clarity
preferred = ['year','date','home_team','away_team',
             'home_team_goals','away_team_goals',
             'goal_difference','winning_team','venue','city','attendance','referee','notes']
order = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
df = df[order]

# 🔟 Save and download cleaned CSV
cleaned_file = "fifa_cleaned_matches_1930_2022.csv"
df.to_csv(cleaned_file, index=False)
print("✅ Cleaned file saved:", cleaned_file, "Shape:", df.shape)
files.download(cleaned_file)

# ✅ Preview
df.head()