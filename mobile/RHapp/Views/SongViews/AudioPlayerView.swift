//
//  AudioPlayerView.swift
//  RHapp
//
//  Created by Nicholas Puig on 3/30/25.
//

import SwiftUI
import AVKit

struct AudioPlayerView: View {
    var url: URL?  // The URL of the audio file
    
    @State private var player: AVAudioPlayer?  // The audio player instance
    @State private var isPlaying = false  // Tracks whether the audio is playing or not
    @State private var totalTime: TimeInterval = 0.0  // Total duration of the audio
    @State private var currentTime: TimeInterval = 0.0  // Current playback time of the audio
    @State private var sliderValue: Double = 0.5
    
    // Format the given time interval to a string in mm:ss format
    private func formatTime(_ time: TimeInterval) -> String {
        let seconds = Int(time) % 60
        let minutes = Int(time) / 60
        return String(format: "%02d:%02d", minutes, seconds)
    }
    
    private func setupAudio(withURL url: URL) {
        do {
            player = try AVAudioPlayer(contentsOf: url)
            player?.prepareToPlay()
            totalTime = player?.duration ?? 0.0
        } catch {
            print("Error loading audio: \(error)")
        }
    }

    // Update the current time of the audio playback
    private func updateProgress() {
        guard let player = player, player.isPlaying else { return }
        currentTime = player.currentTime  // Update the current time state
    }
    
    var body: some View {
        VStack {
            if let player = player {
                Button(action: {
                    // Toggle play/pause state
                    isPlaying.toggle()
                    if isPlaying {
                        player.play()  // Play the audio
                    } else {
                        player.pause()  // Pause the audio
                    }
                }) {
                    // Display play or pause button based on the isPlaying state
                    Image(systemName: isPlaying ? "pause.circle.fill" : "play.circle.fill")
                        .resizable()
                        .font(.largeTitle)
                        .foregroundColor(.white)
                        .frame(width: 45, height: 45)
                }
                .buttonStyle(PlainButtonStyle())
                .offset(x: 150, y: -60)
                HStack {
                    Text("\(formatTime(currentTime))")  // Display the current time
                        .font(Font.custom("Inter", size: 13))
                        .foregroundColor(Color(red: 0.67, green: 0.67, blue: 0.67))
                    Slider(value: Binding(get: {
                        currentTime
                    }, set: { newValue in
                        // Update the player's current time and the currentTime state
                        player.currentTime = newValue
                        currentTime = newValue
                    }), in: 0...totalTime)
                    .accentColor(.white)
                    .frame(width: 250, height: 10)
                    .padding(4)
                    Text("\(formatTime(totalTime))")
                        .font(Font.custom("Inter", size: 13))
                        .foregroundColor(Color(red: 0.67, green: 0.67, blue: 0.67))
                }
                .offset(y: -25)
            }
        }
        .onAppear {
            let thumbImage = UIImage(systemName: "circle.fill")
            UISlider.appearance().setThumbImage(thumbImage, for: .normal)
            // Setup the audio player when the view appears
            if let url = url {
                setupAudio(withURL: url)
            }
        }
        .onReceive(Timer.publish(every: 0.01, on: .main, in: .common).autoconnect()) { _ in
            // Update the progress every 0.01 seconds
            updateProgress()
        }
        .onDisappear {
            // Stop the audio player when the view disappears
            player?.stop()
        }
    }
}

#Preview {
    //AudioPlayerView(url: Bundle.main.url(forResource: "scuse", withExtension: "mp3"))
    SongPlayingView(song: Song(name: "Grace", artist: "Jeff Buckley", albumCover: "grace"))
}
