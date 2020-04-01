# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import os
import lyricsgenius
import random

from userbot.events import register
from userbot import CMD_HELP, GENIUS


@register(outgoing=True, pattern="^.lyrics(?: |$)(.*)")
async def lyrics(lyric):
    if r"-" in lyric.text:
        pass
    else:
        await lyric.edit("`Error: please use '-' as divider for <artist> and <song>`\n"
                         "eg: `Nicki Minaj - Super Bass`")
        return

    if GENIUS is None:
        await lyric.edit(
            "`Provide genius access token to config.py or Heroku Var first!`")
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = lyric.text.split('.lyrics')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except Exception:
            await lyric.edit("`What!?!? Please provide artist and song names`")
            return

    if len(args) < 1:
        await lyric.edit("`Please provide artist and song names`")
        return

    await lyric.edit(f"`Searching lyrics for {artist} - {song}...`")

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lyric.edit(f"Song **{artist} - {song}** not found!")
        return
    if len(songs.lyrics) > 4096:
        await lyric.edit("`Lyrics is too big, view the file to see it.`")
        with open("lyrics.txt", "w+") as f:
            f.write(f"Search query: \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
            )
        os.remove("lyrics.txt")
    else:
        await lyric.edit(f"**Search query**: \n`{artist} - {song}`\n\n```{songs.lyrics}```")
    return


CMD_HELP.update({
    "lyrics":
    ">`.lyrics <artist name> - <song name>`"
    "\nUsage: Get lyrics for song"
})
