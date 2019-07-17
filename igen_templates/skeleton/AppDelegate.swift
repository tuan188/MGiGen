import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?
    var assembler: Assembler = DefaultAssembler()

    func applicationDidFinishLaunching(_ application: UIApplication) {
        Localize.setCurrentLanguage("ja")

        if NSClassFromString("XCTest") != nil { // test
            window?.rootViewController = UnitTestViewController()
            window?.makeKeyAndVisible()
        } else {
            bindViewModel()
        }
    }

    private func bindViewModel() {
        guard let window = window else { return }

        let vm: AppViewModel = assembler.resolve(window: window)
        let input = AppViewModel.Input(loadTrigger: Driver.just(()))
        let output = vm.transform(input)
    }
}
