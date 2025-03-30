//
//  SongPlayingView.swift
//  RHapp
//
//  Created by Nicholas Puig on 3/30/25.
//

import SwiftUI
import AVKit

struct SongPlayingView: View {
    var song: Song
    var url = Bundle.main.url(forResource: "scuse", withExtension: "mp3")
    
    @State private var player: AVAudioPlayer?  // The audio player instance
    @State private var isPlaying = false
    
    var body: some View {
        ZStack() {
            Group {
                ZStack {
                    ZStack {
                        HStack {
                            Image(song.albumCover)
                                .resizable()
                                .frame(width: 70, height: 70)
                                .cornerRadius(5)
                                .padding(.leading, 40)
                                .padding(.trailing, 20)
                            VStack(alignment: .leading) {
                                Text(song.name)
                                    .font(Font.custom("Inter", size: 26).weight(.bold))
                                    .lineSpacing(37)
                                    .foregroundColor(.white)
                                Text(song.artist)
                                    .font(Font.custom("Inter", size: 16))
                                    .lineSpacing(37)
                                    .foregroundColor(.white)
                            }
                            Spacer()
                        }
                        .offset(y: -247)
                        AudioPlayerView(url: Bundle.main.url(forResource: "scuse", withExtension: "mp3"))
                            .offset(y: -174.50)
                    }
                    Group {
                        Rectangle() // visual
                            .foregroundColor(.clear)
                            .frame(width: 231, height: 231)
                            .background(Color(red: 0.85, green: 0.85, blue: 0.85))
                            .offset(x: -0.50, y: -16.50)
                        LyricBox()
                    }
                }
                .frame(width: 430, height: 932)
                .background(Color(red: 0.07, green: 0.07, blue: 0.07));
            }
        }
    }
}

struct LyricBox: View {
    var body: some View {
        Rectangle()
            .foregroundColor(.clear)
            .frame(width: 333, height: 190)
            .background(Color(red: 0.75, green: 0.34, blue: 0))
            .cornerRadius(15)
            .offset(x: -0.50, y: 250)
        Text("There's the moon asking to stay         Long enough for the clouds to fly me away         Well it's my time coming, I'm not afraid, afraid to die")
            .font(Font.custom("Inter", size: 16).weight(.bold))
            .lineSpacing(37)
            .foregroundColor(.white)
            .offset(x: 0.50, y: 249.50)
    }
}

#Preview {
    SongPlayingView(song: Song(name: "Grace", artist: "Jeff Buckley", albumCover: "grace"))
}
