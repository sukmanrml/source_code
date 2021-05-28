from tkinter import E
import pymysql


class Database:
    def connect(self):
        # return pymysql.connect("phonebook-mysql", "dev", "dev", "crud_flask")
        return pymysql.connect(host='localhost', user='root', password='', db='chatbot', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor )

    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM pertanyaan_jawaban order by pertanyaan asc")
            else:
                cursor.execute("SELECT * FROM pertanyaan_jawaban where id = %s order by pertanyaan asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def readpengunjung(self,id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM pengguna order by nama asc")
            else:
                cursor.execute("SELECT * FROM pengguna where id = %s order by nama asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def reademail(self,id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM pertanyaan_jawaban WHERE jawaban = 'belum terjawab' order by pertanyaan asc")
            else:
                cursor.execute("SELECT * FROM pertanyaan_jawaban where id = %s order by pertanyaan asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def readsmtp(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM konfigurasi")
            else:
                cursor.execute("SELECT * FROM konfigurasi where id = %s", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def readstatus(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute("SELECT * FROM pertanyaan_jawaban WHERE status = 'hapus' order by pertanyaan asc")
            else:
                cursor.execute("SELECT * FROM pertanyaan_jawaban where id = %s order by pertanyaan asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def readjawab(self, id):
            con = Database.connect(self)
            cursor = con.cursor()

            try:
                if id == None:
                    cursor.execute("SELECT jawaban FROM pertanyaan_jawaban where jawaban NOT LIKE '%belum terjawab%'")
                else:
                    cursor.execute("SELECT jawaban FROM pertanyaan_jawaban where id = %s", (id,))

                return cursor.fetchall()
            except:
                return ()
            finally:
                con.close()
    
    def insert(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            # cursor.execute("INSERT INTO pertanyaan AS p LEFT JOIN jawaban AS j jawaban(id_pertanyaan,jawaban,username) VALUES(%s, %s, %s)",
            #                (data['id_pertanyaan'], data['jawaban'], data['username'],))
            # cursor.execute("INSERT INTO pertanyaan(pertanyaan) VALUES(%s)",
            #                (data['pertanyaan'],))
            # cursor.execute("INSERT INTO jawaban(jawaban, username) VALUES(%s, %s)",
            #                (data['jawaban'], data['username'],))
            cursor.execute("INSERT INTO pertanyaan_jawaban(pertanyaan,jawaban,penjawab) VALUES(%s, %s, %s)",
                           (data['pertanyaan'], data['jawaban'], data['penjawab'],))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def insertquest(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%Y-%M-%d")
        try:
            cursor.execute("INSERT INTO pertanyaan_jawaban(pertanyaan,nama,email) VALUES(%s, %s, %s)",
                           (data['tanya'], data['nama'], data['email'],))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def insertpengguna(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        from datetime import date

        # from datetime import datetime
        # now = datetime.now()
        # current_date = now.strftime("%Y-%M-%d")
        today = date.today()

        try:
            cursor.execute("INSERT INTO pengguna(nama,email,tanggal) VALUES(%s, %s, %s)",
                           (data['nama'], data['surel'], today,))
            con.commit()
            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            # cursor.execute("UPDATE pertanyaan AS p LEFT JOIN jawaban AS j ON p.id_pertanyaan = j.id_pertanyaan set p.pertanyaan = %s, j.jawaban = %s, j.username = %s where p.id_pertanyaan = %s",
            #                (data['pertanyaan'], data['jawaban'], data['username'], id,))
            cursor.execute("UPDATE pertanyaan_jawaban set pertanyaan = %s, jawaban = %s, penjawab = %s where id = %s",
                           (data['pertanyaan'], data['jawaban'], data['penjawab'], id,))
            con.commit()

            return True
        except Exception as e:
            con.rollback()

            return e
        finally:
            con.close()

    def updatekonf(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        cursor.execute("UPDATE konfigurasi set value = %s WHERE konfigurasi_key = 'email'", (data['emailkonf']))

        cursor.execute("UPDATE konfigurasi set value = %s WHERE konfigurasi_key = 'password'", (data['passwordkonf']))

        cursor.execute("UPDATE konfigurasi set value = %s WHERE konfigurasi_key = 'server'", (data['server']))

        cursor.execute("UPDATE konfigurasi set value = %s WHERE konfigurasi_key = 'mail_port'", (data['port']))
        con.commit()

        try:
            return True
        except Exception as e:
            con.rollback()

            return e
        finally:
            con.close()
            

    def statushapus(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE pertanyaan_jawaban set status = 'hapus' where id = %s",
                           (id))
            con.commit()

            return True
        except Exception as e:
            con.rollback()

            return e
        finally:
            con.close()

    def statusaktif(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE pertanyaan_jawaban set status = 'aktif' where id = %s",
                           ( id))
            con.commit()

            return True
        except Exception as e:
            con.rollback()

            return e
        finally:
            con.close()

    def jumlah(self, id):
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d")
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM jumlah_pengunjung WHERE tanggal = %s", (current_time+'%'))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def chart(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM jumlah_pengunjung ORDER BY tanggal DESC limit 7")
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()     

    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM pertanyaan_jawaban where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def deletestat(self):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM pertanyaan_jawaban where status = 'hapus'")
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()
