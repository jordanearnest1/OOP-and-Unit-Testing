import json
import requests
import webbrowser


##############################
########### PART 1 ###########
##############################


# Creating parent class Media #
class Media:
    def __init__(self, json_dict=None, title="No Title", author="No Author", year="No Year", url = "No URL"): 
        if json_dict is None: 
            self.title = title
            self.author = author
            self.year = year
            self.url = url
        else: 
            if json_dict["wrapperType"] == "track":   # movies and songs have the same wrapper type: "track"
                self.title = json_dict["trackName"]
                self.url = json_dict["trackViewUrl"]
            else:
                self.title = json_dict["collectionName"]
                self.url = json_dict["collectionViewUrl"]

            self.author = json_dict['artistName']
            self.year = json_dict['releaseDate'][0:4]   # indexing into the dictionary to get just the year of release

    def __len__(self):
        return 0

    def __str__(self):
        return "{} by {} ({})".format(self.title, self.author, self.year)


class Song(Media):
    def __init__(self, json_dict=None, title ="No Title", author="No Author", year="No Year", url = "No URL", album = "No Album", genre = "No Genre", track_length = "No Track Length"): ##do i need default values? does this dict go at the end?
        super().__init__(json_dict, title, author, year, url)  
        if json_dict is None:
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            self.album = json_dict["collectionName"]
            self.genre = json_dict["primaryGenreName"]
            self.track_length = json_dict["trackTimeMillis"]

    def __str__(self):
        return super().__str__() + " [" + self.genre + "]"

    def __len__(self):
        try:
            track_length_secs = int(self.track_length / 1000)  # converting the track len from ms to sec
            return track_length_secs  
        except:
            return self.track_length

class Movie(Media):
    def __init__(self, json_dict=None, title ="No Title", author="No Author", year="No Year", url = "No URL", rating ="No Rating", movie_length= "No Movie Length"): ##do i need default values?
        super().__init__(json_dict, title, author, year, url)
        if json_dict is None:
            self.rating = rating
            self.movie_length = movie_length
        else: 
            try:
                self.rating = json_dict['contentAdvisoryRating']
            except:
                self.rating = rating  
            try:
                self.movie_length = json_dict['trackTimeMillis']  
            except:
                self.movie_length = movie_length

    def __str__(self):
        return super().__str__() + " [" + self.rating + "]"

    def __len__(self):
        movie_length_mins = (self.movie_length * 1.66667e-5)   #converting the movie len from ms to min
        return int(movie_length_mins) 


###############################################################
########### PART 3: Create objects from iTunes API ###########
##############################################################


CACHE_FNAME = "proj1_cache.json"

try:
    cachefile= open(CACHE_FNAME, "r").read()
    cachefile.close()
    CACHE_DICTION = json.loads(cachefile)
except:
    CACHE_DICTION = 'no'


def request_to_itunes(search_str):
    baseurl = "https://itunes.apple.com/search"
    params_diction = {}
    params_diction["format"] = "json"
    params_diction["term"] = search_str

    unique_id = params_unique_combo(baseurl, params_diction)

    if CACHE_DICTION != 'no':
        print("Getting data from the cache file")
        return(CACHE_DICTION)
    else:
        print("Making new data request to iTunes' API...")
        results = requests.get(url= baseurl, params = params_diction)
        itunes_data = json.loads(results.text)
        cache_this = itunes_data

        cachefile = open(CACHE_FNAME, "w")
        cachestring = json.dumps(cache_this)
        cachefile.write(cachestring)
        cachefile.close()
        return(itunes_data)


def params_unique_combo(baseurl, params_diction):
    alphabetized_keys = sorted(params_diction.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params_diction[k]))
    unique_combo = baseurl + "_".join(res)
    return unique_combo

####################### QUESTION 4 ###########################

def query_input():
    query_input = input("\nPlease enter a search term, or enter exit to quit: ")
    if query_input != "exit":
        return query_input
    else:
        exit()


##running query

def preview_prompt():
    preview_prompt = input("\nEnter a number for more info, or another search term, or exit: ")
    try:
        return int(preview_prompt)
    except:
        return False


def try_url(url):
    try:
        webbrowser.open_new(url)
        print("Launching: \n {}\nin web browser!".format(url))
    except:
        print("Can't find URL!")


def create_inst_lsts(result_lst):
    othermedia_list = []
    song_list = []
    movie_list = []

    for result in result_lst:   #['results']
        if "kind" in result:

            # print(result)
            if result['kind'] == "song":
                song_list.append(Song(json_dict = result))
            else:
                result["kind"] == "feature-movie"
                movie_list.append(Movie(json_dict = result))
        else:
            othermedia_list.append(Media(json_dict= result))

    return [song_list,movie_list,othermedia_list]
    #{"Song: ": song_list, "Movie: ": movie_list, "Other Media : ": othermedia_list}


##############################
########### PART 4 ###########
##############################


if __name__ == "__main__":

    try: 
        query_input = query_input()
        
        while query_input != "exit":
            request_itunes = request_to_itunes(query_input)

            user_results = request_itunes['results']

            # instance_lst_dict = create_inst_lsts(user_results)
            list_medialists = create_inst_lsts(user_results)
            song_list = list_medialists[0]
            movie_list = list_medialists[1]
            othermedia_list = list_medialists[2]

            total_list = song_list+movie_list+othermedia_list

            printed_num = 1
            if len(song_list) > 0:
                print("SONGS:")
                for i in song_list:
                    print("{} {}".format(printed_num, i))
                    printed_num = printed_num + 1

            if len(movie_list) > 0:
                print("MOVIES:")
                for i in movie_list:
                    print("{}. {}".format(printed_num, i))
                    printed_num = printed_num + 1

            if len(othermedia_list) > 0:
                print("OTHER MEDIA:")
                for i in othermedia_list:
                    print("{} {}".format(printed_num, i))
                    printed_num = printed_num + 1

            preview_num = preview_prompt()

            while preview_num != False:
                if preview_num < len(total_list):
                    try_url(total_list[preview_num - 1].url)
                    preview_num = preview_prompt()

                else:
                    break
            query_input = query_input()
    except:
        print("Bye!")
            # query_input = input("Enter a number for more info, or another search term, or exit: ")
            
