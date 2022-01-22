# load modules
import asyncio
import json
import BSAPI.beatsaver as beatsaver


async def main():

    # tags
    tags = ['tech', 'danceStyle', 'speed', 'balanced', 'challenge', 'accuracy', 'fitness', 'swing', 'nightcore', 'folk', 'family', 'ambient', 'funk', 'jazz', 'classical',
            'soul', 'speedcore', 'punk', 'rb', 'holiday', 'vocaloid', 'jrock', 'trance', 'drumbass', 'Comedy', 'Instrumental', 'Hardcore', 'KPop', 'Indie', 'Techno', 'House', 'Game', 'Film', 'Alt', 'Dubstep', 'Metal', 'Anime', 'HipHop', 'JPop', 'Dance', 'Rock', 'Pop', 'Electronic']

    # make playlist
    for tag in tags:

        # init
        page = -1
        IDs = []
        songs = []

        while(True):

            # increment
            page += 1
            print(f'tag={tag}, page={page:03}')

            # get ranked maplist
            searchResponse = await beatsaver.search_maps(page=page, tags=tag)

            # set songs
            if searchResponse is not None:
                print(searchResponse.docs)
                if (searchResponse.docs is not None) and len(searchResponse.docs) > 0:
                    # get
                    IDs += [x.id for x in searchResponse.docs]
                    songs += [{
                        "songName": x.metadata.songName,
                        "levelAuthorName": x.metadata.songAuthorName,
                        "hash": x.versions[0].hash,
                        "levelid": f"custom_level_{x.versions[0].hash}"
                    } for x in searchResponse.docs]
                else:
                    print(1)
                    break
            else:
                break

            await asyncio.sleep(1/200)

        # read image
        if False:
            with open(f'imgs/{tag}.txt', 'r') as f:
                img = f.read()
        img = ''

        # gen playlist
        fname = f'tag_{tag}.bplist'
        playlist = {
            "customData": {
                "syncURL": f"https://github.com/jundoll/bs-playlist-by-tags/releases/latest/download/{fname}",
                "weighting": 20,
                "customPassText": None
            },
            "playlistTitle": f"tag_{tag}",
            "playlistAuthor": "",
            "songs": songs,
            "image": img
        }

        # save
        with open(f'out/{fname}', 'w') as f:
            json.dump(playlist, f)


if __name__ == '__main__':
    asyncio.run(main())
