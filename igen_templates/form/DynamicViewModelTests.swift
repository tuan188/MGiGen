@testable import {{ project }}
import Dto
import RxSwift
import ValidatedPropertyKit
import XCTest

final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!
    private var disposeBag: DisposeBag!

    // Triggers
    private let loadTrigger = PublishSubject<{{ name }}ViewModel.TriggerType>()
    private let {{ submit }}Trigger = PublishSubject<Void>()
    private let cancelTrigger = PublishSubject<Void>()
    private let dataTrigger = PublishSubject<{{ name }}ViewModel.DataType>()

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase, {{ model_variable }}: {{ model_name }}())

        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete(),
            {{ submit }}Trigger: {{ submit }}Trigger.asDriverOnErrorJustComplete(),
            cancelTrigger: cancelTrigger.asDriverOnErrorJustComplete(),
            dataTrigger: dataTrigger.asDriverOnErrorJustComplete()
        )

        disposeBag = DisposeBag()
        output = viewModel.transform(input, disposeBag: disposeBag)
    }

    func test_loadTrigger_cells_need_reload() {
        // act
        loadTrigger.onNext(.load)
        let (cells, needReload) = output.cells

        // assert
        XCTAssertEqual(cells.count, {{ properties|length }})
        XCTAssertEqual(needReload, true)
    }

    func test_loadTrigger_cells_no_need_reload() {
        // act
        loadTrigger.onNext(.endEditing)
        let (cells, needReload) = output.cells

        // assert
        XCTAssertEqual(cells.count, {{ properties|length }})
        XCTAssertEqual(needReload, false)
    }

    func test_cancelTrigger_dismiss() {
        // act
        cancelTrigger.onNext(())

        // assert
        XCTAssert(navigator.dismissCalled)
    }

    {% for p in properties %}
    func test_dataTrigger_{{ model_variable }}_{{ p.name }}() {
        // act
        let {{ p.name }} = {{ p.type.mock_value }}
        dataTrigger.onNext({{ name }}ViewModel.DataType.{{ p.name }}({{ p.name }}))
        loadTrigger.onNext(.endEditing)
        let (cells, _) = output.cells

        // assert
        let dataType = cells[{{ loop.index0 }}].dataType

        if case let {{ name }}ViewModel.DataType.{{ p.name }}({{ p.name }}) = dataType {
            XCTAssertEqual({{ p.name }}, {{ p.name }})
        } else {
            XCTFail()
        }
    }

    func test_dataTrigger_validate_{{ model_variable }}_{{ p.name }}() {
        // act
        let {{ p.name }} = {{ p.type.mock_value }}
        dataTrigger.onNext({{ name }}ViewModel.DataType.{{ p.name }}({{ p.name }}))
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssert(useCase.validate{{ p.name_title }}Called)
    }

    {% endfor %}
    func test_loadTriggerInvoked_enable_{{ submit }}_byDefault() {
        // act
        loadTrigger.onNext(.load)

        // assert
        XCTAssertEqual(output.is{{ submit_title }}Enabled, true)
    }

    func test_{{ submit }}Trigger_not_{{ submit }}() {
        {% for p in properties %}
        useCase.validate{{ p.name_title }}ReturnValue = ValidationResult.failure(ValidationError(message: ""))
        {% endfor %}

        // act
        {% for p in properties %}
        dataTrigger.onNext({{ name }}ViewModel.DataType.{{ p.name }}({{ p.type.mock_value }}))
        {% endfor %}
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssertEqual(output.is{{ submit_title }}Enabled, false)
        {% for p in properties %}
        XCTAssertEqual(output.{{ p.name }}Validation.isValid, false)
        {% endfor %}
        XCTAssertFalse(useCase.{{ submit }}Called)
    }

    func test_{{ submit }}Trigger_{{ submit }}() {
        // act
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssert(useCase.{{ submit }}Called)
    }

    func test_{{ submit }}Trigger_{{ submit }}_fail_show_error() {
        // arrange
        let {{ submit }}ReturnValue = PublishSubject<Void>()
        useCase.{{ submit }}ReturnValue = {{ submit }}ReturnValue.asObserver()

        // act
        {{ submit }}Trigger.onNext(())
        {{ submit }}ReturnValue.onError(TestError())

        // assert
        XCTAssert(useCase.{{ submit }}Called)
        XCTAssert(output.error is TestError)
    }

}