use strict;
use warnings;
use File::Basename;
my $usage =<<USAGE;
##########################################################
#	Program	:	leu.anno.filter.pl
#	Writer	:	chenyuelong
#	Date	:	2016/5/13
#
#usage	:	
#	perl leu.anno.filter.pl <indir> <database_dir> <out>
#
#########################################################
USAGE
####################################################################
#	NM_information
my %nmid =
(
'NM_000927'=>'1',
'NM_003786'=>'1',
'NM_005157'=>'1',
'NM_001626'=>'1',
'NM_181690'=>'1',
'NM_152424'=>'1',
'NM_001754'=>'1',
'NM_000038'=>'1',
'NM_015338'=>'1',
'NM_000051'=>'1',
'NM_000489'=>'1',
'NM_000633'=>'1',
'NM_001123383'=>'1',
'NM_021946'=>'1',
'NM_004333'=>'1',
'NM_001205293'=>'1',
'NM_004343'=>'1',
'NM_032415'=>'1',
'NM_005188'=>'1',
'NM_170662'=>'1',
'NM_001130852'=>'1',
'NM_053056'=>'1',
'NM_000626'=>'1',
'NM_001785'=>'1',
'NM_000077'=>'1',
'NM_004364'=>'1',
'NM_004380'=>'1',
'NM_022148'=>'1',
'NM_000760'=>'1',
'NM_005214'=>'1',

#'NM_001913'=>'1',
#CUX1替换为下面这个转录本
'NM_181552' => '1',

'NM_000769'=>'1',
'NM_017460'=>'1',
'NM_014953'=>'1',
'NM_001372'=>'1',
'NM_022552'=>'1',
'NM_005228'=>'1',
'NM_001983'=>'1',
'NM_001243432'=>'1',
'NM_001987'=>'1',
'NM_004456'=>'1',
'NM_017709'=>'1',
'NM_033632'=>'1',
'NM_004119'=>'1',
'NM_005211'=>'1',
'NM_002049'=>'1',
'NM_032638'=>'1',
'NM_080425'=>'1',
'NM_000561'=>'1',
'NM_000852'=>'1',
'NM_005343'=>'1',
'NM_002167'=>'1',
'NM_001282386'=>'1',
'NM_002168'=>'1',
'NM_006060'=>'1',
'NM_002185'=>'1',
'NM_002227'=>'1',
'NM_004972'=>'1',
'NM_000215'=>'1',
'NM_001291415'=>'1',
'NM_000222'=>'1',
'NM_001197104'=>'1',
'NM_170606'=>'1',
'NM_004985'=>'1',
'NM_001281435'=>'1',
'NM_145333'=>'1',
'NM_002392'=>'1',
'NM_001145785'=>'1',
'NM_000249'=>'1',
'NM_005373'=>'1',
'NM_005957'=>'1',
'NM_001172566'=>'1',
'NM_000268'=>'1',
'NM_017617'=>'1',
'NM_024408'=>'1',
'NM_002520'=>'1',
'NM_000903'=>'1',
'NM_002524'=>'1',
'NM_012229'=>'1',
'NM_001007792'=>'1',
'NM_006180'=>'1',
'NM_006206'=>'1',
'NM_001015877'=>'1',
'NM_002641'=>'1',
'NM_006218'=>'1',
'NM_000314'=>'1',
'NM_002834'=>'1',
'NM_006265'=>'1',
'NM_000321'=>'1',
'NM_015559'=>'1',
'NM_012433'=>'1',
'NM_005475'=>'1',
'NM_005359'=>'1',
'NM_006306'=>'1',
'NM_005445'=>'1',
'NM_003016'=>'1',
'NM_001042749'=>'1',
'NM_003152'=>'1',
'NM_012448'=>'1',
'NM_001135052'=>'1',
'NM_003200'=>'1',
'NR_001566'=>'1',
'NM_001127208'=>'1',
'NM_000546'=>'1',
'NM_000367'=>'1',
'NM_145725'=>'1',
'NM_006758'=>'1',
'NM_024426'=>'1',
'NM_006297'=>'1',
'NM_005089'=>'1',
'NM_014159'=>'1',
'NM_001429'=>'1',
'NM_001002295'=>'1',
'NM_001165'=>'1',
'NM_018638'=>'1',
'NM_000267'=>'1',
'NM_006445'=>'1',
'NM_139276'=>'1',
'NM_000057'=>'1',
'NM_001363'=>'1',
'NM_016222'=>'1',
'NM_001972'=>'1',
'NM_005263'=>'1',
'NM_006118'=>'1',
'NM_006947'=>'1',
'NM_198253'=>'1',
'NM_005245'=>'1',
 );

#	AMIO_information
my %amin =
(
A=>'Ala',
C=>'Cys',
D=>'Asp',
E=>'Glu',
F=>'Phe',
G=>'Gly',
H=>'His',
I=>'Ile',
K=>'Lys',
L=>'Leu',
M=>'Met',
N=>'Asn',
P=>'Pro',
Q=>'Gln',
R=>'Arg',
S=>'Ser',
T=>'Thr',
V=>'Val',
W=>'Trp',
Y=>'Tyr'
);
###################################################################
die $usage unless @ARGV == 3;
my $indirvcf = shift;
my $database_dir = shift;
my $out = shift;

my %output;
my $name=basename($indir)
$name=(split /\./,$name)[0];

open DB,"$database_dir/leu_database" || die $!;
my %db;
my $gene_number = 1;
while(<DB>){
	s/[\r\n]+//;
	my @elements =split /\t/;
	$db{$elements[1]}{$gene_number} = $_;
	$gene_number++;
}
close DB;

my ($reportidx,$report_title) = &report($database_dir);
my %report_hash = %$reportidx;

    open SNP,"$indirvcf" || die $!;
	open RESULT,">$out/$name-RESULT.xls" || die $!;
	open SD,">$out/$name-SD.xls" || die $!;
	my %psd;
	print SD "附表\n";
    print SD "变异基因\t变异位点(HGVS)\t外显子\t变异频率\t变异类型\t数据库编号(COSMIC)\t功能预测\n";
    print SD "\t\t\t\t\tSIFT\tPolyPhen2\n";
	print RESULT "HGVS\t突变比例\t判断是否报出(decision)\t解读(Interpretation)\t结论(Conclution)\t参考依据(Evidence)\tPMID\t参考文献(Reference)\t备注(Note)";
	my %hot;
	my $snp_title = <SNP>;
	$snp_title =~s/[\r\n]+//;
	my %sdhash;
		while(<SNP>){
		s/[\r\n]+//;
		my @elements =split /\t/;
		next if $elements[5]=~/intronic|[UTR]|intergenic|[stream]/;
		my $percentage = &per($elements[-1]);#
		my $hgvs = &hgvs_f($elements[7],$elements[9],$elements[6]);#
		my $flag = "$elements[0]\_$elements[1]\_$elements[2]\_$elements[3]\_$elements[4]";
		pop @elements;
		pop @elements;
		pop @elements;
		my $is_pass = pop @elements;
		my %snp;
		if(exists $db{$elements[6]}){
			foreach my $num(keys %{$db{$elements[6]}}){
				my @tmps = split /\t/,$db{$elements[6]}{$num};
				my $gene = $tmps[1];
				my $amio_mutation = $tmps[13];
				my $nm_id = $tmps[3];
				my $zf = $tmps[4];
				my $chr = $tmps[5];
				my $loc = $tmps[6];
				my @locs;
				if($loc=~/([\d]+)-([\d]+)/){
					for(my $i = $1;$i<$2;$i++){
						push(@locs,$i);
					}
				}
				else{
					push(@locs,$loc);
				}
				my $base_mutation = $tmps[7];
				my $type = $tmps[8];
				my $out = &clinical($db{$elements[6]}{$num});
				my $arround;
				my $precious;
				my $isArround = 0;
				if($type eq 'indel/snp'){
					foreach my $tmp_loc(@locs){
						if($elements[1] eq $tmp_loc){
							$precious = "$gene\t$tmps[12]\t$elements[3]>$elements[4]\t$amio_mutation\t$tmps[16]\t$nm_id\t$chr\t$tmp_loc\t$zf\t$out\tY\t$elements[0]:$elements[1]:$elements[3]:$elements[4]:$elements[6]\t$elements[8]\t$elements[9]\n";
							$isArround = 1;
							$snp{$gene}{$amio_mutation}{$out}{'+'} = $precious;
							$hot{$flag} = 1;
							last;
						}
						elsif(&arround_f($elements[1],$tmp_loc,$base_mutation,"$elements[3]>$elements[4]","SNP") and $isArround ne '1'){
							$arround = "$gene\t$tmps[12]\t$elements[3]>$elements[4]\t$amio_mutation\t$tmps[16]\t$nm_id\t$chr\t$loc\t$zf\t$out\tN\t$elements[0]:$elements[1]:$elements[3]:$elements[4]:$elements[6]\t$elements[8]\t$elements[9]\n";
							$snp{$gene}{$amio_mutation}{$out}{'-'} = $arround;
							$hot{$flag} = 1;
							$isArround = 2;
						}	
					}	
				}
			}
		}
		my %ip;
		if(exists $report_hash{"report"}{$flag}){
			foreach my $tf(keys %{$report_hash{"report"}{$flag}}){
				$ip{"report"}{$flag}{$tf} = 1;
				my $tmp_out = &insert($tf,$report_hash{"report"}{$flag}{$tf});
				$tmp_out =~s/\bNULL\b/\./g;
				my $sd;
				my @tmps = split /\t/,$hgvs;
				print RESULT "$tmps[0]\t$percentage\t$tmp_out";
				$sd = "$hgvs\t$percentage\t$tmp_out";
                my $t = join("\t",@elements); 
				$t =~s/\bNULL\b/\./g;
                print RESULT "\t$t";
				$sd .="\t$t";
				if(exists $hot{$flag}){
					print RESULT "\thot";
					$sd .= "\thot";
				}
				else{
					print RESULT "\t-";
					$sd .= "\t-";
				}
				if($hgvs ne ".\t/" and ($elements[5] eq 'exonic' or $elements[5]  =~ /splicing/)){
					$sd = &f_sd($sd);
					if(!exists $psd{$sd}){
				#		print  $sd;
						$sdhash{$sd} = 1;
						$psd{$sd} =1;
					}
				}
			}
		}
		if(exists $report_hash{"unreport"}{$flag}){
	        foreach my $tf(keys %{$report_hash{"unreport"}{$flag}}){
				next if exists $ip{"report"}{$flag}{$tf};
				my $tmp_out = &insert($tf,$report_hash{"unreport"}{$flag}{$tf});
				$tmp_out =~s/\bNULL\b/\./g;
				my @tmps = split /\t/,$hgvs;
                print RESULT "$tmps[0]\t$percentage\t$tmp_out";
				my $sd = "$hgvs\t$percentage\t$tmp_out";
                my $t = join("\t",@elements); 
				$t =~s/\bNULL\b/\./g;
                print RESULT "\t$t";
				$sd .= "\t$t";
                if(exists $hot{$flag}){
                    print RESULT "\thot";
					$sd .= "\thot";
                }
                else{
                    print RESULT "\t-";
					$sd .= "\t-";
                }
				if($hgvs ne ".\t/" and ($elements[5] eq 'exonic' or $elements[5]  =~ /splicing/)){
					$sd = &f_sd($sd);
					if(!exists $psd{$sd}){
						#print  $sd;
						$sdhash{$sd} = 1;
						$psd{$sd} =1;
					}
				}
        	}
		}	

		if(!exists $report_hash{"unreport"}{$flag} and !exists $report_hash{"report"}{$flag}){
                my $tmp_out = "\t\t\t\t\t\t\t";
                $tmp_out =~s/\bNULL\b/\./g;
				                $tmp_out =~s/\bNULL\b/\./g;
                my $sd;
				my @tmps = split /\t/,$hgvs;
                print RESULT "$tmps[0]\t$percentage\t$tmp_out";
                $sd = "$hgvs\t$percentage\t$tmp_out";
                my $t = join("\t",@elements); 
                $t =~s/\bNULL\b/\./g;
                print RESULT "\t$t";
                $sd .="\t$t";
                if(exists $hot{$flag}){
                    print RESULT "\thot";
                    $sd .= "\thot";
                }   
                else{
                    print RESULT "\t-";
                    $sd .= "\t-";
                }
                if($hgvs ne ".\t/" and ($elements[5] eq 'exonic' or $elements[5]  =~ /splicing/)){
                    $sd = &f_sd($sd);
                    if(!exists $psd{$sd}){
                        #print  $sd;
						$sdhash{$sd} = 1;
                        $psd{$sd} =1;
                    }
                }
            
		}	
		foreach my $g(keys %snp){
			foreach my $am(keys %{$snp{$g}}){
				foreach my $o(keys %{$snp{$g}{$am}}){
					if(exists $snp{$g}{$am}{$o}{'+'}){
						print HOT $snp{$g}{$am}{$o}{'+'};
					}
					else{
						print HOT $snp{$g}{$am}{$o}{'-'};
					}
				}
			}
		}	
	}
	close SNP;
	while(<INDEL>){
		s/[\r\n]+//;
        my @elements =split /\t/;
		my $flag = "$elements[0]\_$elements[1]\_$elements[2]\_$elements[3]\_$elements[4]";
        my $percentage = &per($elements[-1]);#
        my $hgvs = &hgvs_f($elements[7],$elements[9],$elements[6]);#
        pop @elements;
        pop @elements;
        pop @elements;
        my $is_pass = pop @elements;
        my %snp;
        if(exists $db{$elements[6]}){
            foreach my $num(keys %{$db{$elements[6]}}){
                my @tmps = split /\t/,$db{$elements[6]}{$num};
                my $gene = $tmps[1];
                my $amio_mutation = $tmps[13];
                my $nm_id = $tmps[3];
                my $zf = $tmps[4];
                my $chr = $tmps[5];
                my $loc = $tmps[6];
                my @locs;
                if($loc=~/([\d]+)-([\d]+)/){
                    for(my $i = $1;$i<$2;$i++){
                        push(@locs,$i);
                    }
                }
                else{
                    push(@locs,$loc);
                }
                my $base_mutation = $tmps[7];
                my $type = $tmps[8];
                my $out = &clinical($db{$elements[6]}{$num});
                my $arround;
                my $precious;
                my $isArround = 0;
                if($type eq 'indel/snp'){
                    foreach my $tmp_loc(@locs){
                        if($elements[1] eq $tmp_loc){
                            $precious = "$gene\t$tmps[12]\t$elements[3]>$elements[4]\t$amio_mutation\t$tmps[16]\t$nm_id\t$chr\t$tmp_loc\t$zf\t$out\tY\t$elements[0]:$elements[1]:$elements[3]:$elements[4]:$elements[6]\t$elements[8]\t$elements[9]\n";
                            $isArround = 1;
                            $snp{$gene}{$amio_mutation}{$out}{'+'} = $precious;
							$hot{$flag} =1;
                            last;
                        }
                        elsif(&arround_f($elements[1],$tmp_loc,$base_mutation,"$elements[3]>$elements[4]","INDEL") and $isArround ne '1'){
                            $arround = "$gene\t$tmps[12]\t$elements[3]>$elements[4]\t$amio_mutation\t$tmps[16]\t$nm_id\t$chr\t$loc\t$zf\t$out\tN\t$elements[0]:$elements[1]:$elements[3]:$elements[4]:$elements[6]\t$elements[8]\t$elements[9]\n";
                            $snp{$gene}{$amio_mutation}{$out}{'-'} = $arround;
                            $isArround = 2;
							$hot{$flag} = 1;
                        }
                    }
                }

            }
        }
		my %ip;
        if(exists $report_hash{"report"}{$flag}){
            foreach my $tf(keys %{$report_hash{"report"}{$flag}}){
				$ip{"report"}{$flag}{$tf} = 1;
                my $tmp_out = &insert($tf,$report_hash{"report"}{$flag}{$tf});
				$tmp_out =~s/\bNULL\b/\./g;
				my @tmps = split /\t/,$hgvs;
                print RESULT "$tmps[0]\t$percentage\t$tmp_out";
				my $sd = "$hgvs\t$percentage\t$tmp_out";
				my $t = join("\t",@elements);
				$t =~s/\bNULL\b/\./g;
                print RESULT "\t$t";
				$sd .= "\t$t";
                if(exists $hot{$flag}){
		            print RESULT "\thot";
					$sd .= "\thot";
                }
                else{
                    print RESULT "\t-";
					$sd .= "\t-";
                }
				if($hgvs ne ".\t/" and ($elements[5] eq 'exonic' or $elements[5]  =~ /splicing/)){
					$sd = &f_sd($sd);
					if(!exists $psd{$sd}){
						#print  $sd;
						$sdhash{$sd} = 1;
						$psd{$sd} = 1;
					}
				}
            }
		}
        if(exists $report_hash{"unreport"}{$flag}){
			
	        foreach my $tf(keys %{$report_hash{"unreport"}{$flag}}){
				next if exists $ip{"report"}{$flag}{$tf};
                my $tmp_out = &insert($tf,$report_hash{"unreport"}{$flag}{$tf});
				$tmp_out =~s/\bNULL\b/\./g;
				my @tmps = split /\t/,$hgvs;
                print RESULT "$tmps[0]\t$percentage\t$tmp_out";
				my $sd = "$hgvs\t$percentage\t$tmp_out";
				my $t = join("\t",@elements);
				$t=~s/\bNULL\b/\./g;
				print RESULT "\t$t";
				$sd .= "\t$t";
	            if(exists $hot{$flag}){
	                print RESULT "\thot";
					$sd .= "\thot";
                }
                else{
                    print RESULT "\t-";
					$sd .= "\t-";
                }
				if($hgvs ne ".\t/" and ($elements[5] eq 'exonic' or $elements[5]  =~ /splicing/)){
					$sd = &f_sd($sd);
					if(!exists $psd{$sd}){
				#		print  $sd;
						$sdhash{$sd} = 1;
						$psd{$sd} = 1;
					}
				}
            }
        }
        if(!exists $report_hash{"unreport"}{$flag} and !exists $report_hash{"report"}{$flag}){
                my $tmp_out = "\t\t\t\t\t\t\t";
                $tmp_out =~s/\bNULL\b/\./g;
				my @tmps = split /\t/,$hgvs;
                print RESULT "$tmps[0]\t$percentage\t$tmp_out";
                my $sd = "$hgvs\t$percentage\t$tmp_out";
                my $t = join("\t",@elements);
                $t =~s/\bNULL\b/\./g;
                print RESULT "\t$t";
                $sd .= "\t$t";
                if(exists $hot{$flag}){
                    print RESULT "\thot";
                    $sd .= "\thot";
                }
                else{
                    print RESULT "\t-";
                    $sd .= "\t-";
                }
                if($hgvs ne ".\t/" and ($elements[5] eq 'exonic' or $elements[5] =~ /splicing/)){
                    $sd = &f_sd($sd);
                    if(!exists $psd{$sd}){
                       # print $sd;
						$sdhash{$sd} = 1;
                        $psd{$sd} =1;
                    }
                }
            
        }
        foreach my $g(keys %snp){
            foreach my $am(keys %{$snp{$g}}){
                foreach my $o(keys %{$snp{$g}{$am}}){
                    if(exists $snp{$g}{$am}{$o}{'+'}){
                        print HOT $snp{$g}{$am}{$o}{'+'};
                    }
                    else{
                        print HOT $snp{$g}{$am}{$o}{'-'};
                    }
                }
            }
        }


	}    
	foreach my $tp(sort keys %sdhash){
		my @nm_hgvs=split /\t/,$tp;
		next if @nm_hgvs[1]=~/FLT3\).*?ins\w+/ && @nm_hgvs[2]=~/14/;
		print SD $tp;
	}
	close INDEL;
	close SD;
	close HOT;
	close RESULT;
}


sub insert{
	my $tmp = shift;
	my $st = shift;
	
	my @tmps = split /\t/,$tmp;
	$tmps[7] = $st;
	my @res;
	for(my $i=0;$i<8;$i++){
		push(@res,$tmps[$i]);
	}
	my $result = join("\t",@res);
	return $result;
	
}

sub arround_f{
	my $l_1 = shift;
	my $l_2 = shift;
	my $b_1 = shift;
	my $b_2 = shift;
	my $tp = shift;
		

	if($b_1 ne '' and $b_1 eq $b_2 and $l_1 <=$l_2+10 and $l_1 >=$l_2-10){
		return 1;
	}
	elsif($b_1 eq '' and $l_1 <= $l_2+10 and $l_1 >= $l_2-10){
		return 1;
	}
	else{
		
		return 0;
	}
}
sub clinical{
	my $tmp = shift;
	my @es = split /\t/,$tmp;
	my @rs;
	for(my $i=15;$i<@es;$i++){
		push(@rs,$es[$i]);
	}
	my $result = join("\t",@rs);
	return $result;
}

sub report{
	my $sub_dir = shift;
	my @sub_ds = ("report","unreport");
	my $sub_title;
	my %result;
	foreach my $tmp_d(@sub_ds){
		opendir indir,"$sub_dir/$tmp_d" || die $!;
		my @sub_reports = readdir(indir);
		closedir indir;

		foreach my $tmp_dir(@sub_reports){
			next if $tmp_dir eq '.';
			next if $tmp_dir eq '..';

			open IN,"$sub_dir/$tmp_d/$tmp_dir" || die $!;
			$sub_title = <IN>;
			my @ts = split /\t/,$sub_title;
			$sub_title = "$ts[0]\t$ts[1]\t$ts[2]\t$ts[3]\t$ts[4]\t$ts[5]\t$ts[6]\t$ts[7]";
			while(<IN>){
				s/[\r\n]+//;
				my @elements = split /\t/;
				my $flag = "$elements[8]\_$elements[9]\_$elements[10]\_$elements[11]\_$elements[12]";
				my $sub = $elements[7];
				$elements[7] = "\t";
				my $flag2 = join("\t",@elements);
				if(!exists $result{$tmp_d}{$flag}){
					$result{$tmp_d}{$flag}{$flag2} = $sub;
				}
				else{
					$sub .= ",$result{$tmp_d}{$flag}{$flag2}";
					$result{$tmp_d}{$flag}{$flag2} = $sub;
				}
			}
			close IN;
		}
	}
	return (\%result,$sub_title);
}

sub sp{
	my $tmp = shift;
	my @tmps = split /-/,$tmp;
	my $tmp_sam = shift @tmps;
	my $tmp_lib = join('-',@tmps);
	return ($tmp_sam,$tmp_lib);
}


sub per{
	my $tmp = shift;
	my $result = 0;
	if($tmp =~ /[0|1]\/[1|2]:(?<ref>[\d]+),(?<alt>[\d]+)/){
		my $depth = $+{ref}+$+{alt};
		if $depth==0:
		    $result = 0;
		else{
		   $result = $+{alt}/$depth;
		 }
	}
	else{
		print "Sorry,Cannot calculate the percentage at all!\n$tmp\n";
	}
	$result = $result*100;
	$result =sprintf("%3.2f%%",$result);
	return $result;
}

sub hgvs_f{
	my $tmp1 = shift;##7
	my $tmp2 = shift;##9
	my $gene = shift;##6
	
	return '.' if $tmp1 eq 'NULL' and $tmp2 eq 'NULL';
	if($tmp1 ne 'NULL'){
		my @tmps = split /,/,$tmp1;
		foreach my $t(@tmps){
			my @ts = split /,/,$t;
			foreach $t(@ts){
				if($t =~ /^(NM_[\d]+):(.*):(c\..+)$/ and exists $nmid{$1}){
					return "$1($gene):$3\t/";
				}
			}
		}
	}
	if($tmp2 ne 'NULL'){
		my @tmps = split /,/,$tmp2;
		foreach my $t(@tmps){
#			print "$t\n";
			if($t =~ /^(?<gene>[\w]+):(?<trans>NM_[\d]+):(?<exon>exon[\d]+):(?<base>c\.(?<ref>[\w])(?<loc>[\d]+)(?<alt>[\w])):(?<ami>p.*?)$/ and exists $nmid{$+{trans}}){
				my $out = "$+{trans}($+{gene}):c.$+{loc}$+{ref}>$+{alt}($+{ami})\t$+{exon}";
				$out =~s/exon/Exon /;
				return $out;
#				return "$+{trans}($+{gene}):c.$+{loc}$+{ref}>$+{alt}($+{ami})\t2$exon";
			}
			elsif($t =~ /^(?<gene>[\w]+):(?<trans>NM_[\d]+):(?<exon>exon[\d]+):(?<base>c.*?):(?<ami>p.*?)$/ and exists $nmid{$+{trans}}){
				my $out = "$+{trans}($+{gene}):$+{base}($+{ami})\t$+{exon}";
				$out =~s/exon/Exon /;
				return $out;				
#				return "$+{trans}($+{gene}):$+{base}($+{ami})\t1EXONtest";
			}
		}
	}
	return ".\t/";

}

sub f_sd{
	my $tmp = shift;
	$tmp =~s/[\r\n]+//;
	my @elements = split /\t/,$tmp;
	my $sift = &normal($elements[28]);
	my $cosmic = &normal($elements[65]);
	my $polyphen = &normal($elements[30]);
	my $id = 19;
	if($elements[16] =~/splicing/){
		$id=16;
	}
	my $result = "$elements[17]\t$elements[0]\t$elements[1]\t$elements[2]\t$elements[$id]\t$cosmic\t$sift\t$polyphen\n";
	return $result;
}
sub normal{
	my $tmp = shift;
	if($tmp eq 'NULL'){
		return '.';
	}
	else{
		return $tmp;
	}
}
