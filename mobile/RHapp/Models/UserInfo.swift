//
//  UserInfo.swift
//  RHapp
//
//  Created by Nicholas Puig on 3/29/25.
//

import Foundation
import SwiftUI

struct UserInfo: Identifiable {
    var id = UUID()
    var name: String
    var email: String
    
    init() {
        self.init(name: "", email: "")
    }
    
    init(name: String, email: String) {
        self.name = name
        self.email = email
    }
}
