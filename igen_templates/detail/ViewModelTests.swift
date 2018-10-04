@testable import {{ project }}
import XCTest
import RxSwift
import RxBlocking

final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    private var disposeBag: DisposeBag!
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!
    private let loadTrigger = PublishSubject<Void>()

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase, {{ model_variable }}: {{ model_name }}())
        disposeBag = DisposeBag()
        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete()
        )
        output = viewModel.transform(input)
        output.cells.drive().disposed(by: disposeBag)
    }

    func test_loadTriggerInvoked_createCells() {
        // act
        loadTrigger.onNext(())
        let cells = try? output.cells.toBlocking(timeout: 1).first()

        // assert
        XCTAssertNotEqual(cells??.count, 0)
    }
}
