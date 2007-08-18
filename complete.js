<?php
ob_start("ob_gzhandler");
/**
 * NOTE: Don't be fooled by the extension.  This gets intepreted by the PHP
 * interpreter.  That way I can dispatch based on the query string.
 *
 * See .htaccess for how to configure it for php5.
 */
header("Content-type: text/javascript");
?>

<?php
/* Figure out our base path. */
$me = $_SERVER['SCRIPT_NAME']; // 
$parsed = parse_url($me);
$dirname = dirname($parsed['path']);
$base = 'http://' . $_SERVER['HTTP_HOST'] . $dirname;

/* Load the prerequisite JS files */
$pre_reqs = array('js/safari-label-fix.js', 'js/cc-tooltip.js', 'js/cc-jurisdictions.js', 'js/cc-license.js');
foreach ($pre_reqs as $pre_req) {
	echo file_get_contents($pre_req);
}

/* NOTE: I do not include the CSS stylesheet
   and instead I let others style our boxes the way they want. */

/* Determine which template file the user wanted */

$extras = array();

if ((array_key_exists('jurisdictions', $_GET)) && ($_GET['jurisdictions'] == 'disabled')) {
	$extras[] = 'nojuri';
}
if (array_key_exists('want_a_license', $_GET)) {
	if ($_GET['want_a_license'] == 'definitely') {
		$extras[] = 'definitely_want_license';
	} else if ($_GET['want_a_license'] == 'not_at_start') {
		$extras[] = 'no_license_by_default';
	} else if ($_GET['want_a_license'] == 'at_start') {
		// No extras
		// the license box chooser will be in by default
	}
}

sort($extras);
$extras_string = implode('.', $extras);
if ($extras_string) {
	$template_dot_js = 'template.' . $extras . '.js';
} else {
	$template_dot_js = 'template.js';
}

/* First check if we were called with ?locale=XX and dispatch accordingly */
    if (array_key_exists('locale', $_GET) &&
	// valid locales are lower or upper case alphas plus _ or -
	preg_match('/^([a-zA-Z-_]+)$/', $_GET['locale']))
	{
	    $template_url = $base . '/' . $template_dot_js . '.' . $_GET['locale'];
	}

/* Else, do the generic one and hope they either like English or will
 * do their own language negotiation */
    else {
	$template_url = $base . '/' . $template_dot_js . '.var';
    }
?>

document.write('<script type="text/javascript" src="<?php echo $template_url ?>"></script>\n');
document.write('<script type="text/javascript" src="<?php echo $base ?>/js/init.js"></script>\n')
