import XCTest
@testable import {{ project }}

final class {{ enum.name }}CellTests: XCTestCase {
    var cell: {{ enum.name }}Cell!

    override func setUp() {
        super.setUp()
        cell = {{ enum.name }}Cell.loadFromNib()
    }

    func test_ibOutlets() {
        XCTAssertNotNil(cell)
        XCTAssertNotNil(cell.titleLabel)
    }
}