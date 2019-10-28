//___FILEHEADER___

@testable import ___PROJECTNAME___
import XCTest
import Reusable

final class ___VARIABLE_productName___ViewControllerTests: XCTestCase {
    var viewController: ___VARIABLE_productName___ViewController!
    
    override func setUp() {
        super.setUp()
        viewController = ___VARIABLE_productName___ViewController.instantiate()
    }
    
    func test_ibOutlets() {
        _ = viewController.view
//        XCTAssertNotNil(viewController.tableView)
    }
}
