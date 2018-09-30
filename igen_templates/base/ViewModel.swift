struct {{name}}ViewModel: ViewModelType {
    struct Input {

    }

    struct Output {

    }

    let navigator: {{name}}NavigatorType
    let useCase: {{name}}UseCaseType

    func transform(_ input: Input) -> Output {
        return Output()
    }
}
