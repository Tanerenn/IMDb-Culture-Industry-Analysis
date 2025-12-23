import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12}) 


try:
    df = pd.read_csv('IMDB Top 250 Movies.csv')
except:
    print("Hata: Dosya bulunamadı.")
    exit()


def clean_runtime(row):
    try:
        if isinstance(row, str):
            parts = row.split()
            minutes = 0
            for part in parts:
                if 'h' in part: minutes += int(part.replace('h', '')) * 60
                elif 'm' in part: minutes += int(part.replace('m', ''))
            return minutes
        return None
    except: return None

def clean_money(row):
    try:
        if isinstance(row, str):
            if 'Not Available' in row: return None
            return float(re.sub(r'[^\d]', '', row))
        return row
    except: return None

df['runtime_minutes'] = df['run_time'].apply(clean_runtime)
df['box_office_num'] = df['box_office'].apply(clean_money)
df['genre_list'] = df['genre'].apply(lambda x: [g.strip() for g in x.split(',')] if isinstance(x, str) else [])
df_exploded = df.explode('genre_list')
df_exploded['era'] = df_exploded['year'].apply(lambda x: '2000 Öncesi' if x < 2000 else '2000 Sonrası')


plt.figure(figsize=(10, 6))
sns.regplot(x='year', y='runtime_minutes', data=df, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('Yıllara Göre Film Süreleri ve Standartlaşma Trendi')
plt.xlabel('Yıl')
plt.ylabel('Süre (Dakika)')
plt.tight_layout()
plt.savefig('slide1_sure.png', dpi=300) 
print("1. Grafik hazır: slide1_sure.png")


plt.figure(figsize=(10, 6))
top_genres = df_exploded['genre_list'].value_counts().head(6).index
df_top_genres = df_exploded[df_exploded['genre_list'].isin(top_genres)]
sns.countplot(x='genre_list', hue='era', data=df_top_genres, order=top_genres, palette='Set2')
plt.title('Sinemada Tür Değişimi: Düşünce (Drama) vs Eğlence (Aksiyon)')
plt.xlabel('Tür')
plt.ylabel('Film Sayısı')
plt.legend(title='Dönem')
plt.tight_layout()
plt.savefig('slide2_tur.png', dpi=300)
print("2. Grafik hazır: slide2_tur.png")

plt.figure(figsize=(10, 6))
sns.scatterplot(x='box_office_num', y='rating', data=df, alpha=0.7, s=100, color='purple')
plt.xscale('log')
plt.title('Gişe Hasılatı ve IMDb Puanı İlişkisi')
plt.xlabel('Gişe Hasılatı (Logaritmik)')
plt.ylabel('IMDb Puanı')
plt.tight_layout()
plt.savefig('slide3_gise.png', dpi=300)
print("3. Grafik hazır: slide3_gise.png")
