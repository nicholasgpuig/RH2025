//
//  SongModel.swift
//  RHapp
//
//  Created by Nicholas Puig on 3/30/25.
//

import Foundation

struct Song: Identifiable {
    let id = UUID()
    let name: String
    let artist: String
    let albumCover: String // Image name in assets
}
