@testable import {{project}}
import XCTest

final class {{name}}CellsTests: XCTestCase {
{% for property in properties %}
    private var {{property.name}}Cell: {{model_name}}{{property.name_title}}Cell!
{% endfor %}

    override func setUp() {
        super.setUp()
    {% for property in properties %}
        {{property.name}}Cell = {{model_name}}{{property.name_title}}Cell.loadFromNib()
    {% endfor %}
    }

    func test_ibOutlets() {
    {% for property in properties %}
        XCTAssertNotNil({{property.name}}Cell.{{property.name}}Label)
    {% endfor %}
    }
}
