//
//  SingleSongView.swift
//  RHapp
//
//  Created by Nicholas Puig on 3/30/25.
//

import SwiftUI

struct SearchItem: View {
    var song: Song
    
    var body: some View {
        HStack {
            Image(song.albumCover)
                .resizable()
                .frame(width: 40, height: 40)
                .cornerRadius(5)

            VStack(alignment: .leading) {
                Text(song.name)
                    .font(Font.custom("Inter", size: 16))
                Text(song.artist)
                    .font(Font.custom("Inter", size: 16))
                    .foregroundColor(.gray)
            }
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity)
    }
}
