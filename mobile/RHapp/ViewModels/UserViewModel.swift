//
//  UserViewModel.swift
//  RHapp
//
//  Created by Nicholas Puig on 3/29/25.
//

import Foundation
import SwiftUI

class UserViewModel: ObservableObject {
    @Published var user = UserInfo()
    @Published var circleTabIndex = 0
}
