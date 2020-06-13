import dash_html_components as html


LOGO_STYLE = {
    'position' : 'fixed',
    'top' : 0,
    'left' : 0,
    'width' : '16rem',
    'height' : '5rem',
    'text-align' : 'center',
    'background-color' : '#1E90FF'
}

logo = html.Div(
    [
        html.H2('SAGE', className = 'display-4')
    ],
    style = LOGO_STYLE
)

