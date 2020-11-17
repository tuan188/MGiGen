@testable import {{ project }}
import RxSwift
import XCTest

final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!
    private var disposeBag: DisposeBag!

    // Triggers
    private let loadTrigger = PublishSubject<Void>()
    private let select{{ enum.name }}Trigger = PublishSubject<IndexPath>()

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase)

        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete(),
            select{{ enum.name }}Trigger: select{{ enum.name }}Trigger.asDriverOnErrorJustComplete()
        )

        disposeBag = DisposeBag()
        output = viewModel.transform(input, disposeBag: disposeBag)
    }

    func test_loadTrigger_load{{ enum.name }}List() {
        // act
        loadTrigger.onNext(())

        // assert
        XCTAssertEqual(output.{{ enum.name_variable }}List.count, {{ name }}ViewModel.{{ enum.name }}.allCases.count)
    }

    private func indexPath(of {{ enum.name_variable }}: {{ name }}ViewModel.{{ enum.name }}) -> IndexPath {
        return IndexPath(row: {{ enum.name_variable }}.rawValue, section: 0)
    }

    {% for menu_case in enum.cases_title %}
    func test_select{{ enum.name }}Trigger_to{{ menu_case }}() {
        // act
        loadTrigger.onNext(())
        let indexPath = self.indexPath(of: .{{ enum.cases[loop.index0] }})
        select{{ enum.name }}Trigger.onNext(indexPath)

        // assert
        XCTAssert(navigator.to{{ menu_case }}Called)
    }{{ '\n' if not loop.last }}
    {% endfor %}
}
