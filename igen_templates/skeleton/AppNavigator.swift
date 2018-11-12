import UIKit

protocol AppNavigatorType {

}

struct AppNavigator: AppNavigatorType {
    unowned let assembler: Assembler
    unowned let window: UIWindow
}
