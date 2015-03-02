#!/usr/bin/perl
#=========================================================================

#=========================================================================

use strict;
use vars qw ( $progname $version $version_date $opt_h $opt_m $opt_d
              $heli_product_dir $heli_install_dir $heli_data_dir
              $cmd $result $datenow
              $my_pid
             );

#=========================================================================
# initialize
$| = 1;    #flush stdout
$progname = "run_heli.pl";
$version = "Version 1.00";
$version_date = "Apr. 10, 2014";

$datenow = `date`;
chomp $datenow;
print "$progname $version starting at $datenow\n\n";

# extra debug info for hangs
#print "===============================\n";
#$cmd = "ps -fu agonzales | grep -i 'heli\|python'";
#my @lines = `$cmd`;
#chomp @lines;
#print "Active Python/Heli processes for agonzales\n";
#for (my $i = 0; $i < @lines; $i++) {
#	print "\t$lines[$i]\n";
#}
#print "===============================\n";


# make new heliplots 
generate_heliplots();

# lastly, print timestamp and exit
$datenow = `date`;
chomp $datenow;
print "Exiting at $datenow\n\n";

# exit cleanly
exit 0;


#########################################################
sub run_kill {
  my $shll = $_[0];
  my $prog = $_[1];	 
  $shll = $shll;
  $prog = $prog;
  system($shll, $prog);
  my $exit_return = $? >> 8;
  return $exit_return;
}

sub run_heli {
  my $command = $_[0];
  $command = $command; 
  system($command);
  my $exit_return = $? >> 8;
  return $exit_return;
}  # matches sub run

#########################################################
# cd to the install dir and run HeliPlot.py
sub generate_heliplots {

  # want these to be local
  my ($shll, $kill, $out);
  my ($cmd, $result);
  my $rundir = "/home/ANSSEQ/agonzales/HeliPlotAPI/run_heli"; 
  #my $rundir = "/home/agonzales/Heli/HeliPlotAPI/run_heli";
  #my $rundir = "/Users/agonzales/Documents/ASL_USGS/heli/HeliPlotAPI/run_heli";

  chdir $rundir || die "Cannot cd to $rundir\n";
  print "change directory to $rundir\n";

  print "Killing any running/hanging heli processes...\n"; 
  $shll = "sh";
  $kill = "killHeli.sh";
  $out = run_kill($shll, $kill);
  if ($out != 0) {
     print "Error $out running run_kill()\n";
  } 
  
  $cmd = "./HeliPlot.py 2>&1";
  print "invoke heliplot generation with $cmd\n";
  $result = run_heli($cmd);
  if ($result != 0) {
     print "Error $result running $cmd\n";
  }

  $cmd = "./run_heli_24hr.py 2>&1";
  print "\ninvoke heliplot html generation with $cmd\n";
  $result = run_heli($cmd);
  if ($result != 0) {
     print "Error $result running $cmd\n";
  }

  return;
}  # matches sub generate_heliplots
