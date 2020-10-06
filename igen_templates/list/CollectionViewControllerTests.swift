@testable import {{ project }}
import Reusable
import UIKit
import XCTest

final class {{ name }}ViewControllerTests: XCTestCase {
    private var viewController: {{ name }}ViewController!

    override func setUp() {
		super.setUp()
//        viewController = {{ name }}ViewController.instantiate()
	}

    func test_ibOutlets() {
//        _ = viewController.view
//        XCTAssertNotNil(viewController.collectionView)
    }
}
