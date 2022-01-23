# load modules
import asyncio
import json
import BSAPI.beatsaver as beatsaver


async def main():

    # tags
    TAGS = {
        'genre1': [
            'accuracy',
            'balanced',
            'challenge',
            'dance-style',
            'fitness',
            'speed',
            'tech'
        ],
        'genre2': [
            'alternative',
            'ambient',
            'anime',
            'classical-orchestral',
            'comedy-meme',
            'dance',
            'drum-and-bass',
            'dubstep',
            'electronic',
            'folk-acoustic',
            'funk-disco',
            'hardcore',
            'hip-hop-rap',
            'holiday',
            'house',
            'indie',
            'instrumental',
            'j-pop',
            'j-rock',
            'jazz',
            'k-pop',
            'kids-family',
            'metal',
            'nightcore',
            'pop',
            'punk',
            'rb',
            'rock',
            'soul',
            'speedcore',
            'swing',
            'tv-movie-soundtrack',
            'techno',
            'trance',
            'video-game-soundtrack',
            'vocaloid'
        ]
    }

    # make playlist
    for tag in sum(TAGS.values(), []):

        # init
        page = -1
        songs = []

        while(True):

            # increment
            page += 1
            print(f'tag={tag}, page={page:03}')

            # get ranked maplist
            searchResponse = await beatsaver.search_maps(page=page, tags=tag)

            # set songs
            if searchResponse is not None:
                if (searchResponse.docs is not None) and (len(searchResponse.docs) > 0):
                    # get
                    songs += [{
                        "songName": x.metadata.songName,
                        "levelAuthorName": x.metadata.levelAuthorName,
                        "hash": x.versions[0].hash,
                        "levelid": f"custom_level_{x.versions[0].hash}"
                    } for x in searchResponse.docs if (x.metadata is not None) and (x.versions is not None)]
                else:
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
                "syncURL": f"https://github.com/jundoll/bs-playlist-by-tag/releases/latest/download/{fname}"
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
