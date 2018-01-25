#!use/bin/perl;
use strict;
use warnings;
my $file=shift;
my $title=shift;
my $context=\@ARGV;
my @context=@$context;
open OUT,">$file" || die $!;
my @titles=split /t/,$title;
my $titles=join("\t",@titles);
if ($file=~/-N\.txt/){
    print OUT "$titles";
}
else{
     print OUT "$titles\n";
}

foreach my $ele(@context){
	$ele=~s/\[|\]|\,//g;
	my @eles=split /\\t/,$ele;
	my $element=join("\t",@eles);
	#$ele=sprintf ("%s",$ele);
	print OUT "$element\n";
}
close OUT;
