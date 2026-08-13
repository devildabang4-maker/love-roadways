from flask import Flask, render_template, jsonify, request
import sqlite3, os
app=Flask(__name__); DB=os.path.join(os.path.dirname(__file__),"love_roadways.db")
OLD_CLASSICS=[
("Lag Ja Gale","Lata Mangeshkar","Woh Kaun Thi?","1964","Evergreen",""),
("Ajeeb Dastan Hai Yeh","Lata Mangeshkar","Dil Apna Aur Preet Parai","1960","Evergreen",""),
("Pal Pal Dil Ke Paas","Kishore Kumar","Blackmail","1973","Romantic",""),
("O Mere Dil Ke Chain","Kishore Kumar","Mere Jeevan Saathi","1972","Romantic",""),
("Mere Sapno Ki Rani","Kishore Kumar","Aradhana","1969","Romantic",""),
("Roop Tera Mastana","Kishore Kumar","Aradhana","1969","Romantic",""),
("Yeh Shaam Mastani","Kishore Kumar","Kati Patang","1971","Romantic",""),
("Chura Liya Hai Tumne Jo Dil Ko","Asha Bhosle, Mohammed Rafi","Yaadon Ki Baaraat","1973","Romantic",""),
("Gulabi Aankhen","Mohammed Rafi","The Train","1970","Romantic",""),
("Khaike Paan Banaraswala","Kishore Kumar","Don","1978","Party",""),
("Tere Bina Zindagi Se","Kishore Kumar, Lata Mangeshkar","Aandhi","1975","Sad",""),
("Musafir Hoon Yaaron","Kishore Kumar","Parichay","1972","Travel",""),
("Zindagi Ek Safar Hai Suhana","Kishore Kumar","Andaz","1971","Travel",""),
("Chookar Mere Man Ko","Kishore Kumar","Yaarana","1981","Romantic",""),
("Humein Tumse Pyaar Kitna","Kishore Kumar","Kudrat","1981","Romantic",""),
("Aye Zindagi Gale Laga Le","Suresh Wadkar","Sadma","1983","Evergreen",""),
("Tujhse Naraz Nahi Zindagi","Anup Ghoshal","Masoom","1983","Sad",""),
("Tum Itna Jo Muskura Rahe Ho","Jagjit Singh","Arth","1982","Sad",""),
("Jhuki Jhuki Si Nazar","Jagjit Singh","Arth","1982","Romantic",""),
("Tere Jaisa Yaar Kahan","Kishore Kumar","Yaarana","1981","Friendship",""),
("Papa Kehte Hain","Udit Narayan","Qayamat Se Qayamat Tak","1988","Nostalgia",""),
("Akele Hain To Kya Gham Hai","Udit Narayan, Alka Yagnik","Qayamat Se Qayamat Tak","1988","Romantic",""),
("Gazab Ka Hai Din","Udit Narayan, Alka Yagnik","Qayamat Se Qayamat Tak","1988","Romantic",""),
("Ae Mere Humsafar","Udit Narayan, Alka Yagnik","Qayamat Se Qayamat Tak","1988","Romantic",""),
("Pehla Nasha","Udit Narayan, Sadhana Sargam","Jo Jeeta Wohi Sikandar","1992","Romantic",""),
("Tujhe Dekha To","Kumar Sanu, Lata Mangeshkar","Dilwale Dulhania Le Jayenge","1995","Romantic",""),
("Do Dil Mil Rahe Hain","Kumar Sanu","Pardes","1997","Romantic",""),
("Nazar Ke Samne","Anuradha Paudwal, Kumar Sanu","Aashiqui","1990","Romantic",""),
("Dheere Dheere Se Meri Zindagi","Anuradha Paudwal, Kumar Sanu","Aashiqui","1990","Romantic",""),
("Tu Meri Zindagi Hai","Kumar Sanu, Anuradha Paudwal","Aashiqui","1990","Romantic",""),
("Ab Tere Bin","Kumar Sanu","Aashiqui","1990","Sad",""),
("Ek Ladki Ko Dekha","Kumar Sanu","1942: A Love Story","1994","Romantic","fTauOK8J-U8"),
("Dil Hai Ki Manta Nahin","Kumar Sanu, Anuradha Paudwal","Dil Hai Ke Manta Nahin","1991","Romantic","PQ93X4R0oLg"),
("Mera Dil Bhi Kitna Pagal Hai","Kumar Sanu, Alka Yagnik","Saajan","1991","Romantic","-g6k8OKvwRo"),
("Jiye To Jiye Kaise","Kumar Sanu, Pankaj Udhas, Anuradha Paudwal","Saajan","1991","Sad","0tMo_qkxsHY"),
("Dil To Pagal Hai","Lata Mangeshkar, Udit Narayan","Dil To Pagal Hai","1997","Romantic","lZ2PhyBF3GQ"),
("Pardesi Pardesi","Udit Narayan, Alka Yagnik","Raja Hindustani","1996","Sad","QKfGl39ZJWI"),
("Baazigar O Baazigar","Kumar Sanu, Alka Yagnik","Baazigar","1993","Romantic",""),
("Yeh Kaali Kaali Aankhen","Kumar Sanu, Anu Malik","Baazigar","1993","Party",""),
("Aisi Deewangi","Alka Yagnik, Nadeem-Shravan","Deewana","1992","Romantic",""),
("Sochenge Tumhe Pyar","Kumar Sanu","Deewana","1992","Romantic",""),
("Chura Ke Dil Mera","Kumar Sanu, Alka Yagnik","Main Khiladi Tu Anari","1994","Party",""),
("Kuch Kuch Hota Hai","Udit Narayan, Alka Yagnik","Kuch Kuch Hota Hai","1998","Romantic",""),
("Ladki Badi Anjaani Hai","Kumar Sanu, Alka Yagnik","Kuch Kuch Hota Hai","1998","Romantic",""),
("Aankhon Ki Gustakhiyan","Kumar Sanu, Kavita Krishnamurti","Hum Dil De Chuke Sanam","1999","Romantic",""),
("Tadap Tadap Ke","K. K., Dominique","Hum Dil De Chuke Sanam","1999","Sad",""),
("Chithi Na Koi Sandesh","Jagjit Singh","Dushman","1998","Sad",""),
("Adayein Bhi Hain","Abhijeet, Alka Yagnik","Dil Hai Ke Manta Nahin","1991","Romantic",""),
("Tu Shayar Hai","Alka Yagnik","Saajan","1991","Romantic",""),
("Bahut Pyar Karte Hain","Anuradha Paudwal","Saajan","1991","Romantic",""),
("Main Koi Aisa Geet Gaoon","Abhijeet, Alka Yagnik","Yes Boss","1997","Romantic","")]

def db(): c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
 c=db(); c.execute("CREATE TABLE IF NOT EXISTS songs(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,artist TEXT,movie TEXT,year TEXT,category TEXT,youtube_id TEXT DEFAULT '',favorite INTEGER DEFAULT 0)"); c.execute("DELETE FROM songs WHERE CAST(year AS INTEGER)>=2000"); existing={r[0] for r in c.execute("SELECT title FROM songs")};
 for row in OLD_CLASSICS:
  if row[0] not in existing: c.execute("INSERT INTO songs(title,artist,movie,year,category,youtube_id) VALUES(?,?,?,?,?,?)",row)
 c.commit(); c.close()
init_db()
@app.route("/")
def home():
 c=db(); songs=[dict(x) for x in c.execute("SELECT * FROM songs WHERE CAST(year AS INTEGER)<2000 ORDER BY CAST(year AS INTEGER),id")]; c.close(); return render_template("index.html",songs=songs)
@app.get("/api/songs")
def songs_api():
 q=request.args.get("q","").lower(); cat=request.args.get("category","All"); c=db(); rows=c.execute("SELECT * FROM songs WHERE CAST(year AS INTEGER)<2000 ORDER BY CAST(year AS INTEGER),id"); out=[]
 for r in rows:
  s=dict(r); text=f'{s["title"]} {s["artist"]} {s["movie"]} {s["category"]}'.lower()
  if (not q or q in text) and (cat=="All" or s["category"]==cat): out.append(s)
 c.close(); return jsonify(out)
@app.post("/api/songs")
def add_song():
 d=request.get_json(force=True)
 if not d.get("title") or int(d.get("year",0))>=2000:return jsonify({"error":"Only pre-2000 Bollywood songs are allowed"}),400
 c=db(); cur=c.execute("INSERT INTO songs(title,artist,movie,year,category,youtube_id) VALUES(?,?,?,?,?,?)",[d.get(k,"") for k in ["title","artist","movie","year","category","youtube_id"]]); c.commit(); row=dict(c.execute("SELECT * FROM songs WHERE id=?",(cur.lastrowid,)).fetchone()); c.close(); return jsonify(row)
@app.get("/admin")
def admin():
 c=db(); songs=[dict(x) for x in c.execute("SELECT * FROM songs WHERE CAST(year AS INTEGER)<2000 ORDER BY CAST(year AS INTEGER),id")]; c.close(); return render_template("admin.html",songs=songs)
if __name__=="__main__":app.run(debug=True)
