@testable import {{ project }}
import UIKit
import XCTest

final class {{ name }}CellsTests: XCTestCase {
    
    {% for p in properties %}
    private var {{ p.name }}Cell: {{ name }}{{ p.name_title }}Cell!
    {% endfor %}
    
    override func setUp() {
        super.setUp()
        {% for p in properties %}
        {{ p.name }}Cell = {{ name }}{{ p.name_title }}Cell.loadFromNib()
        {% endfor %}
    }
    
    func test_ibOutlets() {
        {% for p in properties %}
        // {{ p.name_title }} cell
        XCTAssertNotNil({{ p.name }}Cell)
        {% if p.type.name == 'String' %}
        XCTAssertNotNil({{ p.name }}Cell.{{ p.name }}TextField)
        XCTAssertNotNil({{ p.name }}Cell.{{ p.name }}ValidationLabel)
        {% endif %}
        
        {% endfor %}
    }
}