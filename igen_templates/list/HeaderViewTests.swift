@testable import {{ project }}
import XCTest

final class {{ model_name }}HeaderViewTests: XCTestCase {
    var headerView: {{ model_name }}HeaderView!
    
    override func setUp() {
        super.setUp()
//        headerView = {{ model_name }}HeaderView.loadFromNib()
    }
    
    func test_ibOutlets() {
//        XCTAssertNotNil(headerView)
//        XCTAssertNotNil(headerView.titleLabel)
    }
}