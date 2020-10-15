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
    private var {{ model_variable }}: {{ model_name }}!

    // Triggers
    private let loadTrigger = PublishSubject<Void>()

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        {{ model_variable }} = {{ model_name }}()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase, {{ model_variable }}: {{ model_variable }})

        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete()
        )

        disposeBag = DisposeBag()
        output = viewModel.transform(input, disposeBag: disposeBag)
    }

    func test_loadTrigger_{{ model_variable }}() {
        // act
        loadTrigger.onNext(())
        
        // assert
        {% for p in properties %}
        XCTAssertEqual(output.{{ p.name }}, {{ model_variable }}.{{ p.name }})
        {% endfor %}
    }
}
