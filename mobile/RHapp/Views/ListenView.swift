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
//      Text("App Name")
//        .font(Font.custom("Inter", size: 17))
//        .lineSpacing(22)
//        .foregroundColor(.white)
//        .offset(x: -0.50, y: -394)
      ZStack() { // Search bar
        ZStack() {
          Rectangle()
            .foregroundColor(.clear)
            .frame(width: 372, height: 40)
            .background(Color(red: 0.85, green: 0.85, blue: 0.85))
            .cornerRadius(11)
            .offset(x: 0, y: 0)
        }
        .frame(width: 372, height: 40)
        .offset(x: 0, y: 0)
        Text("Search")
          .font(Font.custom("Inter", size: 17))
          .lineSpacing(22)
          .foregroundColor(Color(red: 0.32, green: 0.32, blue: 0.32))
          .offset(x: -123, y: 0)
        Ellipse() // Magnifying
          .foregroundColor(.clear)
          .frame(width: 15, height: 15)
          .overlay(
            Ellipse()
              .inset(by: 1)
              .stroke(Color(red: 0.60, green: 0.60, blue: 0.60), lineWidth: 1)
          )
          .offset(x: -170.50, y: -1.99)
      }
      .frame(width: 372, height: 40)
      .offset(x: 0, y: -341)
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
