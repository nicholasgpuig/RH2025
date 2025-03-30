//
//  HomeView.swift
//  RHapp
//
//  Created by Nicholas Puig on 3/29/25.
//

import SwiftUI

struct ListenView: View {
  var body: some View {
    ZStack() {
        SearchSongView()
      Text("Choose a song to play\nand see it come to life. ")
        .font(Font.custom("Inter", size: 26).weight(.bold))
        .lineSpacing(37)
        .foregroundColor(.white)
        .offset(x: 0, y: -16)
    }
    .frame(width: 430, height: 932)
    .background(Color(red: 0.07, green: 0.07, blue: 0.07));
  }
}

#Preview {
    HomeView().preferredColorScheme(.dark)
}
