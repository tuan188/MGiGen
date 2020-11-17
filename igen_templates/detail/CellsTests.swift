@testable import {{ project }}
import XCTest

final class {{ name }}CellsTests: XCTestCase {
    {% for p in properties %}
    private var {{ p.name }}Cell: {{ model_name }}{{ p.name_title }}Cell!
    {% endfor %}

    override func setUp() {
        super.setUp()
        {% for p in properties %}
//        {{ p.name }}Cell = {{ model_name }}{{ p.name_title }}Cell.loadFromNib()
        {% endfor %}
    }

    func test_ibOutlets() {
        {% for p in properties %}
        // {{ p.name_title }} cell
//        XCTAssertNotNil({{ p.name }}Cell)
//        XCTAssertNotNil({{ p.name }}Cell.{{ p.name }}Label){{ '\n' if not loop.last }}
        {% endfor %}
    }
}
