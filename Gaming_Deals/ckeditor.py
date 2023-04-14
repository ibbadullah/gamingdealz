CKEDITOR_CONFIGS = {
    'ck1': {
        'toolbar': 'Custom',
        'height': '100%',
        'width': '100%',
        'toolbar_Custom': [
            {'name': 'clipboard', 'items': ['Undo', 'Redo']},
            ['Bold', 'Italic', 'Underline'],
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
        ],
    },
    'ck2': {
        'toolbar': 'Custom',
        'height': '100%',
        'width': '100%',
        'toolbar_Custom': [
            {'name': 'clipboard', 'items': ['Undo', 'Redo']},
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Image'],
            {'name': 'styles', 'items':
                ['Styles', 'Format', 'Font', 'FontSize']
             },
        ],
    }
}
