import unittest
import proj1_w18 as proj1
import json

class TestMedia(unittest.TestCase):

    def testMediaConstructor(self):
        m1 = proj1.Media()
        m2 = proj1.Media(title = "1999", author= "Prince")

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")
        self.assertEqual(m1.url, "No URL")
        self.assertEqual(m1.__str__(), "No Title by No Author (No Year)")
        self.assertEqual(m1.__len__(), 0)

        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")
        self.assertEqual(m2.__str__(), "1999 by Prince (No Year)")
        self.assertEqual(m2.__len__(), 0)


class TestSong(unittest.TestCase):
    def testSongConstructor(self):
        s1 = proj1.Song()
        s2 = proj1.Song(title = "Hey Jude", author = "The Beatles", year= "1968", album = "The Beatles 1967-1970 (The Blue Album)", genre= "Rock", track_length = 331000, url = "No URL")  ##am i creating objects by hand correctly

        self.assertEqual(s1.title, "No Title")
        self.assertEqual(s1.author, "No Author")
        self.assertEqual(s1.year, "No Year")
        self.assertEqual(s1.album, "No Album")
        self.assertEqual(s1.genre, "No Genre")
        self.assertEqual(s1.url, "No URL")
        self.assertEqual(s1.track_length, "No Track Length")
        self.assertEqual(s1.__str__(), "No Title by No Author (No Year) [No Genre]")
        self.assertEqual(s1.__len__(), "No Track Length")

        self.assertEqual(s2.title, "Hey Jude")
        self.assertEqual(s2.author, "The Beatles")
        self.assertEqual(s2.year, "1968")
        self.assertEqual(s2.album, "The Beatles 1967-1970 (The Blue Album)")
        self.assertEqual(s2.genre, "Rock")
        self.assertEqual(s2.url, "No URL")
        self.assertEqual(s2.track_length, 331000)

        self.assertEqual(s2.__str__(), "Hey Jude by The Beatles (1968) [Rock]")
        self.assertEqual(s2.__len__(), 331)


class TestMovie(unittest.TestCase):
    def testMovieConstructor(self):
        m3 = proj1.Movie()
        m4 = proj1.Movie(title ="Jaws", author= "Steven Spielberg", year= "1975", rating= "PG", movie_length = 7451455, url = "No URL")

        self.assertEqual(m3.title, "No Title")
        self.assertEqual(m3.author, "No Author")
        self.assertEqual(m3.year, "No Year")
        self.assertEqual(m3.rating, "No Rating")
        self.assertEqual(m3.movie_length, "No Movie Length")
        self.assertEqual(m3.url, "No URL")
        self.assertEqual(m3.__str__(), "No Title by No Author (No Year) [No Rating]")
       
        self.assertEqual(m4.title, "Jaws")
        self.assertEqual(m4.author, "Steven Spielberg")
        self.assertEqual(m4.year, "1975")
        self.assertEqual(m4.rating, "PG")
        self.assertEqual(m4.movie_length, 7451455)
        self.assertEqual(m4.url, "No URL")
        self.assertEqual(m4.__str__(), "Jaws by Steven Spielberg (1975) [PG]")
  

sample_json_lst = json.load(open("sample_json.json"))

class TestJsonDict(unittest.TestCase):
    def testMediaInstances(self):
        m1 = proj1.Media(json_dict = sample_json_lst[2])
        self.assertEqual(m1.title, "Bridget Jones's Diary (Unabridged)")
        self.assertEqual(m1.author, "Helen Fielding")
        self.assertEqual(m1.year, "2012")
        self.assertEqual(m1.__str__(), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")
        self.assertEqual(m1.__len__(), 0)

    def testSongInstances(self):
        s1 = proj1.Song(json_dict = sample_json_lst[1])
        self.assertEqual(s1.title, "Hey Jude")
        self.assertEqual(s1.author, "The Beatles")
        self.assertEqual(s1.year, "1968")
        self.assertEqual(s1.album, "TheBeatles 1967-1970 (The Blue Album)")
        self.assertEqual(s1.genre, "Rock")
        self.assertEqual(s1.track_length, 431333)
        self.assertEqual(s1.__str__(), "Hey Jude by The Beatles (1968) [Rock]")
        self.assertEqual(s1.__len__(), 431)


    def testMovieInstances(self):
        m2 = proj1.Movie(json_dict = sample_json_lst[0])
        self.assertEqual(m2.title, "Jaws")
        self.assertEqual(m2.author, "Steven Spielberg")
        self.assertEqual(m2.year, "1975")
        self.assertEqual(m2.rating, "PG")
        self.assertEqual(m2.movie_length, 7451455)
        self.assertEqual(m2.__str__(), "Jaws by Steven Spielberg (1975) [PG]")
        self.assertEqual(m2.__len__(), 124)

        

class TestAPI(unittest.TestCase):
    def testQueries(self):
        data1 = proj1.request_to_itunes("baby") 
        user_search_results1 = data1["results"] 
        results_dict1 = proj1.create_inst_lsts(user_search_results1) 

        num1 = 0
        for category in results_dict1:
            for instance in category:
                num1 += 1

        self.assertLessEqual(num1, 50)
        data2 = proj1.request_to_itunes("helter skelter") 
        user_search_results2 = data2["results"]
        results_dict2 = proj1.create_inst_lsts(user_search_results2)

        num2 = 0
        for category in results_dict2:
            for instance in category:
                num2 += 1

        self.assertLessEqual(num2, 50)
        data3 = proj1.request_to_itunes("&@#!$") 
        user_search_results3 = data3["results"] 
        results_dict3 = proj1.create_inst_lsts(user_search_results3) 

        num3 = 0
        for category in results_dict3:
            for instance in category:
                num3 += 1

        self.assertLessEqual(num3, 50)
        data4 = proj1.request_to_itunes(" ")
        user_search_results4 = data4["results"]
        results_dict4 = proj1.create_inst_lsts(user_search_results4) 

        num4 = 0
        for category in results_dict4:
            for instance in category:
                num4 += 1

        self.assertLessEqual(num4, 50)


unittest.main()



# #############  might not need the following lines?
## The following is a line to run all of the tests you include:
if __name__ == "__main__":
	unittest.main(verbosity=2)


