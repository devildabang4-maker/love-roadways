
from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), "love_roadways.db")

SEED = [
("Dil Hai Ki Manta Nahin","Kumar Sanu, Anuradha Paudwal","Dil Hai Ke Manta Nahin","1991","90s Classics","PQ93X4R0oLg"),
("Ek Ladki Ko Dekha","Kumar Sanu","1942: A Love Story","1994","Romantic","fTauOK8J-U8"),
("Mera Dil Bhi Kitna Pagal Hai","Kumar Sanu, Alka Yagnik","Saajan","1991","90s Classics","-g6k8OKvwRo"),
("Tumse Milna","Kumar Sanu, Alka Yagnik","Tere Naam","2003","Romantic","uP0cj4iGQMg"),
("Kisi Se Tum Pyaar Karo","Kumar Sanu, Alka Yagnik","Andaaz","2003","Romantic","-lDmXk8pBNI"),
("Dil To Pagal Hai","Lata Mangeshkar, Udit Narayan","Dil To Pagal Hai","1997","90s Classics","lZ2PhyBF3GQ"),
("Pardesi Pardesi","Udit Narayan, Alka Yagnik","Raja Hindustani","1996","90s Classics","QKfGl39ZJWI"),
("Dil Ne Yeh Kaha Hai Dil Se","Alka Yagnik, Kumar Sanu, Sonu Nigam","Dhadkan","2000","Romantic","MFommhp4XVk"),
("Jiye To Jiye Kaise","Kumar Sanu, Pankaj Udhas, Anuradha Paudwal","Saajan","1991","90s Classics","0tMo_qkxsHY"),
("Tere Naam","Udit Narayan, Alka Yagnik","Tere Naam","2003","2000s","OMoU0Pfibc4"),
]

# 90 additional catalog entries. Add an embeddable/authorized YouTube ID from the admin panel.
CATALOG = [
("Pehla Nasha","Udit Narayan, Sadhana Sargam","Jo Jeeta Wohi Sikandar","1992","Romantic"),
("Tujhe Dekha To","Kumar Sanu, Lata Mangeshkar","DDLJ","1995","Romantic"),
("Aankhon Ki Gustakhiyan","Kumar Sanu, Kavita Krishnamurti","Hum Dil De Chuke Sanam","1999","Romantic"),
("Chura Ke Dil Mera","Kumar Sanu, Alka Yagnik","Main Khiladi Tu Anari","1994","Party"),
("Humko Humise Chura Lo","Lata Mangeshkar, Udit Narayan","Mohabbatein","2000","Romantic"),
("Do Dil Mil Rahe Hain","Kumar Sanu","Pardes","1997","90s Classics"),
("Ae Kash Ke Hum","Kumar Sanu","Kabhi Haan Kabhi Naa","1994","90s Classics"),
("Yeh Kaali Kaali Aankhen","Kumar Sanu, Anu Malik","Baazigar","1993","Party"),
("Baazigar O Baazigar","Kumar Sanu, Alka Yagnik","Baazigar","1993","90s Classics"),
("Main Koi Aisa Geet Gaoon","Abhijeet, Alka Yagnik","Yes Boss","1997","Romantic"),
("Suno Na Suno Na","Abhijeet, Alka Yagnik","Chalte Chalte","2003","Romantic"),
("Aisi Deewangi","Alka Yagnik, Nadeem-Shravan","Deewana","1992","90s Classics"),
("Sochenge Tumhe Pyar","Kumar Sanu","Deewana","1992","Romantic"),
("Kuch Kuch Hota Hai","Udit Narayan, Alka Yagnik","Kuch Kuch Hota Hai","1998","90s Classics"),
("Ladki Badi Anjaani Hai","Kumar Sanu, Alka Yagnik","Kuch Kuch Hota Hai","1998","Romantic"),
("Saajanji Ghar Aaye","Kavita Krishnamurti, Kumar Sanu","Kuch Kuch Hota Hai","1998","Party"),
("Koi Mil Gaya","Udit Narayan, Kavita Krishnamurti","Kuch Kuch Hota Hai","1998","Party"),
("Sajan Sajan O Mere Sajan","Alka Yagnik, Kumar Sanu, Sapna Awasthi","Dil Ka Rishta","2003","Romantic"),
("Adayein Bhi Hain","Abhijeet, Alka Yagnik","Dil Hai Ke Manta Nahin","1991","Romantic"),
("O Mere Sapno Ke Saudagar","Alka Yagnik","Dil Hai Ke Manta Nahin","1991","Romantic"),
("Tu Shayar Hai","Alka Yagnik","Saajan","1991","Romantic"),
("Bahut Pyar Karte Hain","Anuradha Paudwal","Saajan","1991","Romantic"),
("Dekha Hai Pehli Baar","Alka Yagnik, S. P. Balasubrahmanyam","Saajan","1991","Romantic"),
("Nazar Ke Samne","Anuradha Paudwal, Kumar Sanu","Aashiqui","1990","90s Classics"),
("Dheere Dheere Se Meri Zindagi","Anuradha Paudwal, Kumar Sanu","Aashiqui","1990","Romantic"),
("Tu Meri Zindagi Hai","Kumar Sanu, Anuradha Paudwal","Aashiqui","1990","Romantic"),
("Jaane Jigar Jaaneman","Anuradha Paudwal, Kumar Sanu","Aashiqui","1990","Romantic"),
("Ab Tere Bin","Kumar Sanu","Aashiqui","1990","Sad"),
("Chithi Na Koi Sandesh","Jagjit Singh","Dushman","1998","Sad"),
("Tadap Tadap Ke","K. K., Dominique","Hum Dil De Chuke Sanam","1999","Sad"),
("Aankh Hai Bhari Bhari","Kumar Sanu","Tum Se Achcha Kaun Hai","2002","Sad"),
("Sach Keh Raha Hai Deewana","K. K.","Rehnaa Hai Terre Dil Mein","2001","Sad"),
("Zara Zara","Bombay Jayashri","Rehnaa Hai Terre Dil Mein","2001","Romantic"),
("Kaho Naa Pyaar Hai","Udit Narayan, Alka Yagnik","Kaho Naa... Pyaar Hai","2000","2000s"),
("Na Tum Jaano Na Hum","Lucky Ali, Ramya","Kaho Naa... Pyaar Hai","2000","Romantic"),
("Aaja Mahiya","Udit Narayan, Alka Yagnik, Prashant Samaddar","Fiza","2000","Party"),
("Pyaar Ki Kashti Mein","Udit Narayan, Alka Yagnik","Kaho Naa... Pyaar Hai","2000","Party"),
("Chand Sifarish","Shaan, Kailash Kher","Fanaa","2006","Romantic"),
("Mere Haath Mein","Sonu Nigam, Sunidhi Chauhan","Fanaa","2006","Romantic"),
("Tere Bina","A. R. Rahman, Chinmayi","Guru","2007","Romantic"),
("Aankhon Mein Teri","K. K.","Om Shanti Om","2007","Romantic"),
("Ajab Si","K. K.","Om Shanti Om","2007","Romantic"),
("Main Agar Kahoon","Sonu Nigam, Shreya Ghoshal","Om Shanti Om","2007","Romantic"),
("Tum Se Hi","Mohit Chauhan","Jab We Met","2007","Romantic"),
("Aao Milo Chalo","Shaan, Ustad Sultan Khan","Jab We Met","2007","Party"),
("Mauja Hi Mauja","Mika Singh","Jab We Met","2007","Party"),
("Tujh Mein Rab Dikhta Hai","Roop Kumar Rathod, Shreya Ghoshal","Rab Ne Bana Di Jodi","2008","Romantic"),
("Haule Haule","Sukhwinder Singh","Rab Ne Bana Di Jodi","2008","Romantic"),
("Pee Loon","Mohit Chauhan","Once Upon a Time in Mumbaai","2010","Romantic"),
("Tum Jo Aaye","Rahat Fateh Ali Khan, Tulsi Kumar","Once Upon a Time in Mumbaai","2010","Romantic"),
("Iktara","Kavita Seth","Wake Up Sid","2009","Romantic"),
("Khaabon Ke Parinday","Mohit Chauhan, Alyssa Mendonsa","Zindagi Na Milegi Dobara","2011","Travel"),
("Senorita","Farhan Akhtar, Hrithik Roshan, Abhay Deol","Zindagi Na Milegi Dobara","2011","Travel"),
("Phir Se Ud Chala","Mohit Chauhan","Rockstar","2011","Travel"),
("Kun Faya Kun","A. R. Rahman, Javed Ali, Mohit Chauhan","Rockstar","2011","Classics"),
("Tum Ho","Mohit Chauhan, Suzanne D'Mello","Rockstar","2011","Romantic"),
("Agar Tum Saath Ho","Alka Yagnik, Arijit Singh","Tamasha","2015","Romantic"),
("Matargashti","Mohit Chauhan","Tamasha","2015","Travel"),
("Ilahi","Arijit Singh","Yeh Jawaani Hai Deewani","2013","Travel"),
("Kabira","Tochi Raina, Rekha Bhardwaj","Yeh Jawaani Hai Deewani","2013","Romantic"),
("Badtameez Dil","Benny Dayal","Yeh Jawaani Hai Deewani","2013","Party"),
("Dilliwali Girlfriend","Arijit Singh, Sunidhi Chauhan","Yeh Jawaani Hai Deewani","2013","Party"),
("Samjhawan","Arijit Singh, Shreya Ghoshal","Humpty Sharma Ki Dulhania","2014","Romantic"),
("Manwa Laage","Arijit Singh, Shreya Ghoshal","Happy New Year","2014","Romantic"),
("Gerua","Arijit Singh, Antara Mitra","Dilwale","2015","Romantic"),
("Janam Janam","Arijit Singh, Antara Mitra","Dilwale","2015","Romantic"),
("Hawayein","Arijit Singh","Jab Harry Met Sejal","2017","Romantic"),
("Raabta","Arijit Singh","Agent Vinod","2012","Romantic"),
("Tum Hi Ho","Arijit Singh","Aashiqui 2","2013","Romantic"),
("Chahun Main Ya Naa","Arijit Singh, Palak Muchhal","Aashiqui 2","2013","Romantic"),
("Sun Raha Hai","Ankit Tiwari","Aashiqui 2","2013","Sad"),
("Hum Mar Jayenge","Arijit Singh, Tulsi Kumar","Aashiqui 2","2013","Romantic"),
("Tera Ban Jaunga","Akhil Sachdeva, Tulsi Kumar","Kabir Singh","2019","Romantic"),
("Kaise Hua","Vishal Mishra","Kabir Singh","2019","Romantic"),
("Bekhayali","Sachet Tandon","Kabir Singh","2019","Sad"),
("Shayad","Arijit Singh","Love Aaj Kal","2020","Romantic"),
("Ranjha","B Praak, Jasleen Royal","Shershaah","2021","Romantic"),
("Maan Meri Jaan","King","Champagne Talk","2022","Romantic"),
("Kesariya","Arijit Singh","Brahmastra","2022","Romantic"),
("Apna Bana Le","Arijit Singh","Bhediya","2022","Romantic"),
("Tere Vaaste","Varun Jain, Shadab Faridi, Altamash Faridi","Zara Hatke Zara Bachke","2023","Romantic"),
("O Maahi","Arijit Singh","Dunki","2023","Romantic"),
("Satranga","Arijit Singh","Animal","2023","Romantic"),
("Aaj Ki Raat","Madhubanti Bagchi, Divya Kumar, Sachin-Jigar","Stree 2","2024","Party"),
("Tauba Tauba","Karan Aujla","Bad Newz","2024","Party"),
("Apna Bana Le","Arijit Singh","Bhediya","2022","Party"),
("What Jhumka?","Arijit Singh, Jonita Gandhi","Rocky Aur Rani Kii Prem Kahaani","2023","Party"),
("Ve Kamleya","Arijit Singh, Shreya Ghoshal","Rocky Aur Rani Kii Prem Kahaani","2023","Romantic"),
("Tum Kya Mile","Arijit Singh, Shreya Ghoshal","Rocky Aur Rani Kii Prem Kahaani","2023","Romantic"),
("Heeriye","Jasleen Royal, Arijit Singh","Heeriye","2023","Romantic"),
("Tere Pyaar Mein","Arijit Singh, Nikhita Gandhi","Tu Jhoothi Main Makkaar","2023","Party"),
("Pehle Bhi Main","Vishal Mishra","Animal","2023","Romantic"),
("Sajni","Arijit Singh","Laapataa Ladies","2024","Romantic"),
("Chaleya","Arijit Singh, Shilpa Rao","Jawan","2023","Romantic"),
("Not Ramaiya Vastavaiya","Anirudh Ravichander, Vishal Dadlani, Shilpa Rao","Jawan","2023","Party"),
("Zinda Banda","Anirudh Ravichander","Jawan","2023","Party"),
("Soni Soni","Darshan Raval, Jonita Gandhi","Ishq Vishk Rebound","2024","Romantic"),
("Aaj Ki Raat","Madhubanti Bagchi, Divya Kumar, Sachin-Jigar","Stree 2","2024","Party"),
("Ve Haaniyaan","Avvy Sra, Danny, Sagar","Ve Haaniyaan","2024","Romantic"),
]

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c=db()
    c.execute("""CREATE TABLE IF NOT EXISTS songs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL, artist TEXT, movie TEXT, year TEXT,
        category TEXT, youtube_id TEXT DEFAULT '', favorite INTEGER DEFAULT 0
    )""")
    count=c.execute("SELECT COUNT(*) FROM songs").fetchone()[0]
    if count == 0:
        for row in SEED:
            c.execute("INSERT INTO songs(title,artist,movie,year,category,youtube_id) VALUES(?,?,?,?,?,?)", row)
        for row in CATALOG:
            c.execute("INSERT INTO songs(title,artist,movie,year,category,youtube_id) VALUES(?,?,?,?,?,?)", (*row,""))
        c.commit()
    c.close()

init_db()

@app.route("/")
def home():
    c=db()
    songs=[dict(x) for x in c.execute("SELECT * FROM songs ORDER BY id").fetchall()]
    c.close()
    return render_template("index.html", songs=songs)

@app.get("/api/songs")
def songs_api():
    q=request.args.get("q","").strip().lower()
    category=request.args.get("category","All")
    c=db()
    rows=c.execute("SELECT * FROM songs ORDER BY id").fetchall()
    c.close()
    out=[]
    for r in rows:
        s=dict(r)
        text=f'{s["title"]} {s["artist"]} {s["movie"]} {s["category"]}'.lower()
        if q and q not in text: continue
        if category != "All" and s["category"] != category: continue
        out.append(s)
    return jsonify(out)

@app.post("/api/songs")
def add_song():
    data=request.get_json(force=True)
    required=["title","artist","movie","year","category","youtube_id"]
    if not data.get("title"): return jsonify({"error":"title required"}),400
    c=db()
    cur=c.execute("""INSERT INTO songs(title,artist,movie,year,category,youtube_id)
                     VALUES(?,?,?,?,?,?)""", [data.get(k,"") for k in required])
    c.commit()
    row=dict(c.execute("SELECT * FROM songs WHERE id=?",(cur.lastrowid,)).fetchone())
    c.close()
    return jsonify(row)

@app.put("/api/songs/<int:song_id>")
def update_song(song_id):
    data=request.get_json(force=True)
    fields=["title","artist","movie","year","category","youtube_id"]
    c=db()
    c.execute("""UPDATE songs SET title=?,artist=?,movie=?,year=?,category=?,youtube_id=?
                 WHERE id=?""", [data.get(k,"") for k in fields]+[song_id])
    c.commit()
    row=c.execute("SELECT * FROM songs WHERE id=?",(song_id,)).fetchone()
    c.close()
    return jsonify(dict(row)) if row else (jsonify({"error":"not found"}),404)

@app.delete("/api/songs/<int:song_id>")
def delete_song(song_id):
    c=db()
    c.execute("DELETE FROM songs WHERE id=?",(song_id,))
    c.commit(); c.close()
    return jsonify({"ok":True})

@app.post("/api/songs/<int:song_id>/favorite")
def favorite(song_id):
    c=db()
    row=c.execute("SELECT favorite FROM songs WHERE id=?",(song_id,)).fetchone()
    if not row: c.close(); return jsonify({"error":"not found"}),404
    new=0 if row["favorite"] else 1
    c.execute("UPDATE songs SET favorite=? WHERE id=?",(new,song_id))
    c.commit(); c.close()
    return jsonify({"favorite":new})

@app.get("/admin")
def admin():
    c=db(); songs=[dict(x) for x in c.execute("SELECT * FROM songs ORDER BY id").fetchall()]; c.close()
    return render_template("admin.html", songs=songs)

if __name__=="__main__":
    app.run(debug=True)
