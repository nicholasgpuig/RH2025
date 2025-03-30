//
//  HomeView.swift
//  RHapp
//
//  Created by Nicholas Puig on 3/29/25.
//

import SwiftUI

struct ListenView: View {
    @State private var selectedSong: Song? = nil
    @FocusState private var isSearchFocused: Bool
    @State private var searchText: String = ""
    @State private var showDropdown: Bool = false
    
    let songs: [Song] = [
        Song(name: "Grace", artist: "Jeff Buckley", albumCover: "grace"),
        Song(name: "Fallen Angel", artist: "King Crimson", albumCover: "red"),
        Song(name: "range brothers", artist: "Baby Keem", albumCover: "keem")
    ]
    
    var filteredSongs: [Song] {
        if searchText.isEmpty {
            return []
        } else {
            return songs.filter { $0.name.lowercased().contains(searchText.lowercased())
            }
        }
    }
    
  var body: some View {
    ZStack() {
        VStack {
            ZStack {
                RoundedRectangle(cornerRadius: 11)
                    .fill(Color.gray.opacity(0.5))
                    .frame(width: 372, height: 40)

                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(.gray)
                        .padding(.leading, 10)

                    TextField("Search", text: $searchText, onEditingChanged: { editing in
                        withAnimation { showDropdown = editing }
                    })
                    .focused($isSearchFocused)
                    .font(.custom("Inter", size: 17))
                    .foregroundColor(.white)
                    .frame(height: 40)

                    Spacer()
                }
                .padding(.horizontal, 10)
            }
            .frame(width: 372, height: 40)
            .overlay(
                VStack(spacing: 0) {
                    if showDropdown && !filteredSongs.isEmpty {
                        VStack(spacing: 0) {
                            ScrollView {
                                VStack(spacing: 0) {
                                    ForEach(filteredSongs) { song in
                                        SearchItem(song: song)
                                        .onTapGesture {
                                            selectedSong = song // Fill search bar with song name
                                                showDropdown = false   // Hide dropdown
                                                isSearchFocused = false
                                            }
                                    }
                                }
                            }
                            .frame(height: 220) // Set fixed height for the dropdown
                            .clipped() // Ensures scrolling stays within the frame
                        }
                        .frame(width: 372)
                        .background(Color(red: 74.0 / 255, green: 74.0 / 255, blue: 74.0 / 255))
                        .cornerRadius(10)
                        .shadow(radius: 5)
                    }
                }
                .offset(y: 45), // Moves dropdown below search bar
                alignment: .topLeading
            )
        }
        .offset(x: 0, y: -341)
        .padding()
        .zIndex(1)
        // END OF SEARCH BAR
        
        if let song = selectedSong {
            SongPlayingView(song: song)
                .zIndex(0)
        } else {
            Text("Choose a song to play\nand see it come to life. ")
              .font(Font.custom("Inter", size: 26).weight(.bold))
              .lineSpacing(37)
              .foregroundColor(.white)
              .offset(x: 0, y: -16)
        }
    }
    .frame(width: 430, height: 932)
    .background(Color(red: 0.07, green: 0.07, blue: 0.07))
    .onTapGesture {
        dismissKeyboard()
    }
  }
    private func dismissKeyboard() {
            isSearchFocused = false // Reset SwiftUI focus state
            UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
        }
}

#Preview {
    HomeView().preferredColorScheme(.dark)
}
