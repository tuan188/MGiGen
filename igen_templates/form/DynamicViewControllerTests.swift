@testable import {{ project }}
import Reusable
import XCTest

final class {{ name }}ViewControllerTests: XCTestCase {
    var viewController: {{ name }}ViewController!

    override func setUp() {
        super.setUp()
//        viewController = {{ name }}ViewController.instantiate()
    }

    func test_ibOutlets() {
//        _ = viewController.view
//        XCTAssertNotNil(viewController.tableView)
//        XCTAssertNotNil(viewController.cancelButton)
//        XCTAssertNotNil(viewController.{{ submit }}Button)
    }
}