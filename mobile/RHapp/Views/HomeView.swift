//
//  ContentView.swift
//  RHapp
//
//  Created by Nicholas Puig on 3/29/25.
//

import SwiftUI

struct HomeView: View {
    @ObservedObject var viewModel = UserViewModel()
    @State var tabIndex: Int = 0
    
    var body: some View {
        NavigationStack{
            TabView(selection: $tabIndex) {
                ListenView()
                    .tabItem({
                        Label("Home", systemImage: "house")
                    }).tag(0)
                DrawView()
                    .tabItem({
                        Label("Draw", systemImage: "paintpalette")
                    }).tag(1)
                LibraryView()
                    .tabItem({
                        Label("Your Library", systemImage: "books.vertical")
                    }).tag(2)
            }
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Image("misc")
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .clipShape(Circle())
                        .frame(width: 45)
                        .overlay {
                            Circle()
                                .strokeBorder(.gray, lineWidth: 1)
                    }
                        .padding()
                }
                ToolbarItem(placement: .principal) {
                    Text("App Name")
                        .font(Font.custom("Inter", size: 25).weight(.bold))
                        .foregroundStyle(.white)
                }
            }
            .navigationBarTitleDisplayMode(.inline)
        }
        .navigationBarBackButtonHidden(true)
        .environmentObject(viewModel)
    }
}

#Preview {
    HomeView().preferredColorScheme(.dark)
}
