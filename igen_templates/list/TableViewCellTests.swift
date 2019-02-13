@testable import {{ project }}
import XCTest

final class {{ model_name }}CellTests: XCTestCase {
    var cell: {{ model_name }}Cell!

    override func setUp() {
        super.setUp()
//        cell = {{ model_name }}Cell.loadFromNib()
    }

    func test_ibOutlets() {
//        XCTAssertNotNil(cell)
        {% for p in properties %}
//        XCTAssertNotNil(cell.{{ p.name }}Label)
        {% endfor %}
    }
}
