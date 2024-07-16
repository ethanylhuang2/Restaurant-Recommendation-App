//
//  ContentView.swift
//  restaurant-recommendation
//
//  Created by Ethan Huang on 7/1/24.
//

import SwiftUI
import Combine

let yelpAPIKey = "ZdpeG8xFeTZRSqqiNnbe6tvcV9OI6FKenEdeuEpMLuUhq41DQ9EX9-71yKGfsIvxW9mYIzqZznCG2AuECKuQVOmGUvti485q_e_dS4OxSi3ZCSqwcABXYhdjyr9oZnYx"

struct Restaurant : Identifiable {
    let id: Int
    let name: String
    let imageName: String
    var rating: Int
}


struct ContentView: View {
    @State private var restaurant = Restaurant(id: 1, name: "Hello", imageName: "none", rating: 0)

    var body: some View {
        ZStack {
            Image(restaurant.imageName)
                .resizable()
                .scaledToFill()
                .edgesIgnoringSafeArea(.all)
                .overlay(
                    Rectangle()
                        .foregroundColor(.black)
                        .opacity(0.7)
                        .edgesIgnoringSafeArea(.all)
                )
                
            VStack {
                Text(restaurant.name)
                    .font(.largeTitle)
                    .foregroundColor(.white)
                    .padding()
                    
                Spacer()
                    .frame(height: 150)
                
                HStack {
                    ForEach(1..<6) { star in
                        Image(systemName: star <= restaurant.rating ? "star.fill" : "star")
                            .resizable()
                            .frame(width: 40, height: 40)
                            .foregroundColor(star <= restaurant.rating ? .yellow : .gray)
                                .onTapGesture {
                                    restaurant.rating = star
                                }
                        }
                    }
                }
            }
        }
}

#Preview {
    ContentView()
}
