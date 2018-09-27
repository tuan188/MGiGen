@testable import {{project}}
import XCTest

final class {{model_name}}CellTests: XCTestCase {
    var cell: {{model_name}}Cell!

    override func setUp() {
        super.setUp()
//        cell = {{model_name}}Cell.loadFromNib()
    }

    func test_iboutlets() {
//        XCTAssertNotNil(cell)
        {% for property in properties %}
//        XCTAssertNotNil(cell.{{property.name}}Label)
        {% endfor %}
    }
}
