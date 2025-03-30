//
//  SearchSongView.swift
//  RHapp
//
//  Created by Nicholas Puig on 3/30/25.
//

import SwiftUI

struct SearchSongView: View {
    
    @State private var searchText: String = ""
    @State private var showDropdown: Bool = false
    @FocusState private var isSearchFocused: Bool // Tracks focus state
    
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
                                        SingleSongView(song: song)
                                        .onTapGesture {
                                                searchText = song.name // Fill search bar with song name
                                                showDropdown = false   // Hide dropdown
                                                dismissKeyboard()
                                            }
                                    }
                                }
                            }
                            .frame(height: 220) // Set fixed height for the dropdown
                            .clipped() // Ensures scrolling stays within the frame
                        }
                        .frame(width: 372)
                        .background(Color.gray.opacity(0.5))
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
    }
    
    private func dismissKeyboard() {
            isSearchFocused = false // Reset SwiftUI focus state
            UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
        }
}

struct ContentView: View {
    var body: some View {
        SearchSongView()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView().preferredColorScheme(.dark)
    }
}
