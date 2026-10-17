from . import check_environment, diagnostics, import_result, open_output, run_pipeline, runtime, setup_runtime


def register() -> None:
    runtime.register()
    check_environment.register()
    setup_runtime.register()
    run_pipeline.register()
    import_result.register()
    open_output.register()
    diagnostics.register()


def unregister() -> None:
    runtime.unregister()
    diagnostics.unregister()
    open_output.unregister()
    import_result.unregister()
    run_pipeline.unregister()
    setup_runtime.unregister()
    check_environment.unregister()
